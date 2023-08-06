# TODO pipe stdin to allow manual reindex and svn updates
# report number of cache entries before each cache cleaning to graphite

import os, subprocess, sys, time
import logging; logging.basicConfig(level = logging.DEBUG if os.environ['DEBUG'].lower() == 'true' or '--debug' in sys.argv[:2] else logging.INFO, stream = sys.stdout, format = "%(asctime)-25s %(levelname)-8s %(name)s | %(message)s"); from logging import debug, info, warn, error

firstRepo = 2 if '--debug' in sys.argv[:2] else 1
REPOS, METAS = zip(*[tuple(_.split(",")) for _ in sys.argv[firstRepo:]] if len(sys.argv) > firstRepo else (os.getcwd(), os.getcwd()))  # indexed folder trees to search
PYTHON = os.path.realpath(sys.executable) if sys.platform != 'win32' else '"' + os.path.realpath(sys.executable) + '"'
CACHE = os.path.join(os.getcwd(), "http", "cache")

def call(command): return subprocess.Popen(command, shell = True, bufsize = 1, stdout = sys.stdout, stderr = sys.stderr)

def clearCache():
  for file in os.listdir(CACHE):
    try: os.unlink(file)
    except: logging.warn("Cannot remove cache entry " + repr(file))

logging.info("Starting tagsPlorer HTTP server supervisor")
clearCache()
while True:  # infinite loop
  # First thing each night (or at first start) is to update the source, then re-create all indexes
  logging.info("Updating tagsPlorer source code base")  # but keeps custom files present and merges local modifications
  if call("svn up").wait() != 0: logging.error("Error updating source code base (svn missing?), continuing with previous code base")
  for repo, meta in zip(REPOS, METAS):
    logging.info("Indexing repository '%s' from configuration '%s'" % (repo, meta))
    if call(PYTHON + " tp.py -r %s -i %s -uv" % (repo, meta)).wait() != 0: logging.error("Error indexing repository %s" % repo)
  logging.info("Starting tagsPlorer HTTP server process(es)")
  p = call(PYTHON + " serve.py " + " ".join([r + "," + m for (r, m) in zip(REPOS, METAS)]))  # TODO allow sending SIGINT from the supervisor (e.g. for nightly restart)
  while True:
    time.sleep(300.)  # 5 minutes waiting
    p.poll()
    # TODO check state: if exited - break
    # TODO check hour of day, clearCache() an recreate index every night, break
logging.info("Shut down tagsPlorer HTTP server supervisor")
