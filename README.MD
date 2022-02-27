# Arc.codes PDF File Generation

### An AWS lambda python serverless application that creates translatable PDF files, written with arc.codes, python and Weasyprint, there is also a python library license checker

#### How to run, make sure docker is installed, https://www.docker.com/get-started, and simply run the following command:
`docker compose up`
 
* To aid with local development, mark src as sources root

### When the server comes online visit the following urls: 
* http://localhost:3333/generate-pdf?locale=en
* http://localhost:3333/generate-pdf?locale=de
* http://localhost:3333/check-pyhon-licenses
* http://localhost:3000/ <--- This is the Development UI
  * Note: running UI build enables latest UI at http://localhost:3333/
    * Build **MUST** happen prior to deployment

### Building the UI for production:
  * `npm build` from the arc-pdf-ui folder, requires npm to be installed
  * Alternatively with the docker container running: 
    * `docker exec architectpdf-ui-1 npm run build -d`
  
