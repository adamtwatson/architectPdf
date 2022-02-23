@app
architectPdf

@http
get /generate-pdf
get /check-python-licenses

@aws
profile default
region us-west-1
runtime python3.9