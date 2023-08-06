''' tagsPlorer web portal  (C) 2016-2021  Arne Bachmann  https://github.com/ArneBachmann/tagsplorer '''

# TODO: second index listing is indented
# IDEA: render site, show hourglass and return search result asynchronously (requires spawning separate process, difficult to keep track of?)
# TODO: on timeout inside index still return anything - needs refactoring in findFolders/findFiles
# TODO: add HTTPS https://github.com/goya191/SimpleAuthServerSSL.py/blob/master/SimpleHttpsAuthServer.py

import base64, hashlib, logging, os, sys, socket, time, urllib, urllib2

logging.basicConfig(
  level =  logging.DEBUG if '-V' in sys.argv or '--debug'   in sys.argv or os.environ.get("DEBUG",   "False").lower() == "true" else
          (logging.INFO  if '-v' in sys.argv or '--verbose' in sys.argv or os.environ.get("VERBOSE", "False").lower() == "true" else
           logging.WARNING),  # must be set here to already limit writing to info and debug (e.g. "Started at...")
  stream = sys.stdout if '--stdout' in sys.argv else sys.stderr,  # log to stderr, write results to stdout
  format =  '%(asctime)-5s.%(msecs)03d  %(levelname)-7s  %(module)s:%(funcName)s:%(lineno)d | %(message)s',
  datefmt = '%M:%S')

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from tagsplorer import constants
from tagsplorer.lib import Indexer
from tagsplorer.utils import safeSplit, sjoin, splitByPredicate

_log = logging.getLogger(__name__)
def log(func): return (lambda *s: func(sjoin([_() if callable(_) else _ for _ in s]), **({"stacklevel": 2} if sys.version_info >= (3, 8) else {})))
debug, info, warn, error = log(_log.debug), log(_log.info), log(_log.warning), log(_log.error)

# Custom imports of tagsPlorer
from tp import commaArgsIntoList, DOT, findRootFolder, isglob, removeTagPrefixes, withoutFilesAndGlobs, xany


# Globals
LOGIN = 'ly'
PASSWORD = 'search'
SERVER = ('', 8000)  # localhost with given port
# SEARCHER = ('', 8001)  # asynchronous search server
HTTP = "http"  # folder with resources to serve (and nothing else)
CACHE = os.path.join(HTTP, "cache")
RESOURCES = set([file for file in os.listdir(HTTP)])  # resources allowed to get (whitelist to prevent attacks)
MAX_WAIT = 3.  # maximum time in seconds per query (for all indexes in total)
MAX_SHOW = 250  # maximum number of items to show
CREDENTIALS = base64.b64encode("%s:%s" % (LOGIN, PASSWORD))
MASK =\
  '''
  <form action="/search" method="get" name="search">
  <p>Search terms:
  <input type="text" name="q" id="query" value="%s" />&nbsp;
  Case-sensitive:&nbsp;
  <input type="checkbox" name="case" value="1" %s />
  <input type="submit" />&nbsp;
  <!-- span class="query-hint">Hint: Separate search terms by comma, exclude terms with minus, use dot to find file extensions, use ? and * for file globbing (slow).</span -->
  </p>
  </form>
  '''
mime = {
  "html": "text/html",
  "css": "text/css",
  "js": "application/javascript",
  "pdf": "application/pdf",
  "png": "application/png"
}

# Functions
def sanitize(s): return "".join([_ for _ in s if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.*,"])  # s.replace("&", "&amp;")

def getResource(suffix): return 'custom' + suffix if 'custom' + suffix in RESOURCES else 'default' + suffix

def header():
  with open(os.path.join(HTTP, getResource("_header.xhtml")), 'rb') as fd: return fd.read().replace("${JS}", getResource(".js")).replace("${CSS}", getResource(".css"))

def title(name): return '<h1>' + name + '</h1>'

def footer():
  with open(os.path.join(HTTP, getResource("_footer.xhtml")), 'rb') as fd: return fd.read()


# Main class
class Handler(SimpleHTTPRequestHandler):

  def __init__(_, request, address, server):
    debug("Request from " + str(address))
    try: SimpleHTTPRequestHandler.__init__(_, request, address, server)
    except socket.error as E: error("Connection error, probably aborted by client: " + str(E))

  def log_message(_, format, *args):
    info(" ".join(args))

  def startTime(_):
    _.time = time.time()

  def endTime(_):
    info("Finished after %.3fms" % (1000. * (time.time() - _.time)))

  def end_headers(_, filename = ""):
    _.send_header('Content-type', mime.get(filename[filename.index(".") + 1:] if "." in filename[1:1] else "html", "html"))
    BaseHTTPRequestHandler.end_headers(_)

  def do_AUTHHEAD(_):
    _.send_response(401)
    _.send_header('WWW-Authenticate', 'Basic realm="LY datalake file search"')
    _.end_headers()

  def do_POST(_):
    _.send_response(405); _.end_headers()
    _.wfile.write(header() + title("POST queries not supported.") + MASK % ('', '') + footer())

  def do_GET(_):
    _.startTime()
    if _.headers.getheader('Authorization') == None:  # no authentication posted yet: ask user
      _.do_AUTHHEAD()
      _.wfile.write('<h1>No login credentials received in authorization header.</h1>')
      _.endTime()
      return
    elif _.headers.getheader('Authorization') != 'Basic ' + CREDENTIALS:  # wrong username/password combination entered: ask again
      try: info("Login attempt from %r" % base64.b64decode(_.headers.getheader('Authorization').split(" ")[1]))
      except: error("Couldn't decode authorization string")
      _.do_AUTHHEAD()
      _.wfile.write('<h1>Wrong credentials received in authorization header.</h1>')
      _.endTime()
      return
    # From here on, we're authorized
    if _.path in ["", "/"]:  # start page
      _.send_response(200); _.end_headers()
      _.wfile.write(header() + title("Perform a search") + MASK % ('', '') + footer())

    elif _.path[0] == '/' and _.path[1:] in RESOURCES:  # get resource
      if not os.path.exists(os.path.join(HTTP, _.path[1:])):
        _.send_response(404); _.end_headers()
        _.wfile.write(header() + title("Perform a search") + MASK % ('', '') + footer())
        _.endTime()
        return
      _.send_response(200); _.end_headers(_.path)
      with open(os.path.join(HTTP, _.path[1:])) as fd: _.wfile.write(fd.read())

    elif _.path.startswith("/search?q="):  # perform query
      global hashcache
      _.send_response(200); _.end_headers()
      search = _.path[_.path.index("=") + 1:]
      case = "&" in search and search.split("&")[1] == 'case=1'  # other parameters follow
      if case: search = search.split("&")[0]  # isolate search term itself
      search = urllib.unquote(search)
      if len(search) == 0: _.wfile.write(header() + title("@%s &rarr; No search term(s) given") % time.strftime("%H:%M:%S") + MASK % ('', 'checked="checked"' if case else '') + footer()); _.endTime(); return

      # Perform search
      search = safeSplit(sanitize(search).replace(" ", ","))
      debug("Sanititzed search terms (unsorted): %s" % search)
      poss, negs = splitByPredicate(commaArgsIntoList(search), lambda e: e[0] != '-')
      poss, negs = removeTagPrefixes(poss, negs)
      cacheString = ",".join(sorted(poss) + ["_"] + sorted(negs) + ["+" if case else "-"])
      hasher = hashlib.md5(); hasher.update(cacheString)  # create unique order of search terms
      cachehash = hasher.hexdigest()[:8]
      debug("Cache key and hash for search terms (sorted): '%s' (%s)" % (cacheString, cachehash))
      cachefile = os.path.join(CACHE, cachehash)
      if cachehash in hashcache and os.path.exists(cachefile):
        debug("Sending cached result")
        with open(cachefile, 'rb') as fd: _.wfile.write(fd.read()); debug("Finished sending cached result for '%s' (%s)" % (cacheString, cachehash))
        _.endTime()
        return
      with open(cachefile, 'wb') as fd:  # create new cache entry while searching TODO may be locked by other process: wait and read contents
        debug("Starting search for " + cacheString)
        hashcache.add(cachehash)  # memorize new entry as "known"
#        poss, negs = removeTagPrefixes(poss, negs)
        tmp = header() + "<p>Search criteria:\n<ul><li><span class='cursive'>Must match:</span> %s</li><li><span style='font-style:italic'>Must not match:</span> %s</li></ul></p>" % (", ".join(['"' + p + '"' for p in poss]), ", ".join(['"' + n + '"' for n in negs])) + MASK % (",".join(search), 'checked="checked"' if case else '')
        tmp += title("Search results")
        _.wfile.write(tmp); fd.write(tmp); _.wfile.flush()  # TODO check if flush really speeds up browser rendering?
        for repo in idx:  # for every repository
          init = time.time()
          shown = 0
          debug("Finding folders on '%s'..." % repo.root)
          repo.cfg.case_sensitive = case  # update search option flag (in-memory only, not persisting)
          folders = repo.findFolders(withoutFilesAndGlobs(poss), withoutFilesAndGlobs(negs))
          if len(folders) == 0 and xany(lambda x: isglob(x) or DOT in x, poss + negs): folders = repo.findFolders([], [], True)  # return all folders names unfiltered (except ignore/skip without marker files)
          skipped = []
          foundcount = 0
          debug("Filtering folders... ")
          for folder, (files, skip) in ((path, repo.findFiles(path, poss, negs)) for path in folders):
            if skip: skipped.append(folder); debug("Storing skip information for %r" % folder); continue  # memorize to skip all folders with this path prefix (from skip marker)
            if any([folder.startswith(skp) if skp != '' else (folder == '') for skp in skipped]): debug("Skipping folder", folder); continue  # is in skipped folder tree
            if len(files) > 0: foundcount += 1  # tmp = "<p class='mono fat'>" + repo.root + folder + "</p>\n<ul>"; _.wfile.write(tmp); fd.write(tmp)  # found something in this path
            for file in files: tmp = "<p class ='mono fat'>%s<a href='file://%s'>%s</a></p>" % (folder + os.sep, urllib2.quote(repo.root + folder[1 if repo.root.endswith("/") else 0:] + os.sep + file), file); _.wfile.write(tmp); fd.write(tmp)
            shown += len(files)
            if shown > MAX_SHOW: tmp = "<p class='fat emph'>@%s &rarr; Too many matches for %s, aborting search of this index for now.</p>" % (time.strftime("%H:%M:%S"), repo.root); _.wfile.write(tmp); fd.write(tmp); break
            if len(files) > 0: tmp = "</ul>"; _.wfile.write(tmp); fd.write(tmp); _.wfile.flush()
            if (time.time() - init) > MAX_WAIT / len(idx): tmp = "<p class='fat emph'>@%s &rarr; Database timed out for <span class='mono'>%s</span></p>" % (time.strftime("%H:%M:%S"), repo.root); _.wfile.write(tmp); fd.write(tmp); break  # folder loop
          if foundcount == 0: tmp = "<p class='fat emph'>@%s &rarr; Nothing found for <span class='mono'>%s</a></p>" % (time.strftime("%H:%M:%S"), repo.root); _.wfile.write(tmp); fd.write(tmp)
        tmp = footer(); _.wfile.write(tmp); fd.write(tmp)
      debug("Finished search for " + ",".join(search))
    else:  # unknown REST path
      warn("SPAM REQUEST: " + repr(_.path))
      _.send_response(404); _.end_headers()
      _.wfile.write(header() + title("@%s &rarr; No access to this URL, please use provided search box") % time.strftime("%H:%M:%S") + MASK % ('', '') + footer())
    _.endTime()


# Main entry point
if __name__ == '__main__':
  if len(sys.argv) < 2 or "--help" in sys.argv:
    print("serve.py repopath1,configpath1 repopath2,configpath2 ...")
    sys.exit(0)
  if len(sys.argv) > 1:
    REPOS, METAS = zip(*[tuple(_.split(",")) for _ in sys.argv[1:]])  # indexed folder trees to search
  else:
    rootFolder = findRootFolder(None, constants.CONFIG)
    if rootFolder is None: error("Cannot automatically determine repository path. Please provide a list of REPOPATH,CONFIGPATH pairs as script arguments"); sys.exit(1)
    REPOS, METAS = [os.path.dirname(rootFolder)], [os.path.dirname(rootFolder)]

  idx = [Indexer(repo) for repo in REPOS]  # create index objects with location of storage
  for r, repo in enumerate(idx): repo.index = METAS[r]  # set location of metadata
  for r, repo in enumerate(idx): repo.load(os.path.join(METAS[r], constants.INDEX), True, False)  # load indexes
  for repo in idx: logging.info("Pre-filling path cache for %s" % repo.root); repo.findFolders([], [], True)  # trigger path cache filling - TODO hacky...
  hashcache = set()  # define global variable
  server = HTTPServer(SERVER, Handler)
  info("Starting HTTP server loop")
  while True: server.handle_request()
