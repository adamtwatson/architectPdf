@app
arc-pdf

@http
get /generate-pdf
get /check-python-licenses

@static
fingerprint true
folder ui/build
# By default, Architect ignores .DS_Store, node_modules, and readme.md files
ignore
  .tar.gz
  tmp
  user
@aws
profile default
region us-east-1
runtime python3.9