# Arc.codes PDF File Generation
| ![Tests](tests-badge.svg) | ![Coverage](coverage-badge.svg) | ![Flake8](flake8-badge.svg) |
|:-------------------------:|:-------------------------------:|:---------------------------:|

### Local Development:
Ensure docker is installed: [Docker](https://www.docker.com/get-started)
* run the following command: `docker compose up`
* #### To aid with local development, mark src as sources root

### When the server comes online visit the following urls: 
* http://localhost:3333/generate-pdf?locale=en
* http://localhost:3333/generate-pdf?locale=de
* http://localhost:3333/check-python-licenses
* http://localhost:3000/ <--- This is the Development UI
  * Note: running UI build enables latest UI at http://localhost:3333/
    * Build **MUST** happen prior to deployment

### Building the UI for production:
From the ui folder, *requires npm to be installed*:
  * `npm build` 
  * Alternatively with the docker container running: 
    * `docker exec architectpdf_ui npm run build -d`
  
### Deploying to Production:
* Ensure AWS Credentials are installed
* Deploy to Staging:
  * arc deploy
  * arc deploy --name [your name]
* Deploy to Production:
  * `arc deploy production`

### Coverage and Tests
* Coverage and Test Reports can be found under the `/reports` directory, [here](reports)
* Update Coverage and Test by running the following command `docker exec architectpdf_api ./update_test_coverage_reports.sh`