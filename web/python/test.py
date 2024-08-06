import os

def generate_subsystem_page(subsystem_path, plots, output_dir):
    subsystem_name = os.path.basename(subsystem_path)
    subsystem_html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{subsystem_name}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
      </head>
      <body>
        <nav class="navbar navbar-expand navbar-dark" style="background-color: #070c49;">
          <div class="container-fluid">
            <a class="nav-link h5" href="../index.html">
              <div class="nav-text">
                <b>Home</b>
              </div>
            </a>
          </div>
        </nav>
        <div class="container">
          <h1>{subsystem_name}</h1>
          <div class="row">
    """
    for plot in plots:
        subsystem_html += f"""
            <div class="col-md-4">
              <img src="{plot}" class="img-fluid" alt="{plot}">
            </div>
        """
    subsystem_html += """
          </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
      </body>
    </html>
    """

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(subsystem_html)

def generate_main_page(directory, output_dir):
    main_html = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Key4hep validation</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
      </head>
      <body>
        <nav class="navbar navbar-expand navbar-dark" style="background-color: #070c49;">
          <div class="container-fluid">
            <a class="nav-link h5" href="index.html">
              <div class="nav-text">
                <b>Home</b>
              </div>
            </a>
          </div>
        </nav>
        <p>This is a webpage for validation of Key4hep software. The validation is done automatically and runs in Gitlab CI. The results are stored in EOS and published to this webpage.</p>
        <p>For selecting different detectors and geometries, click the button below to expand a list of available options.</p>
        <h1>Simulation and reconstruction</h1>
        <p>
          <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#foldersList" aria-expanded="false" aria-controls="foldersList">
            Detector, geometry and process
          </button>
        </p>
        <div class="collapse" id="foldersList">
    """

    for detector in os.listdir(directory):
        detector_path = os.path.join(directory, detector)
        if os.path.isdir(detector_path):
            main_html += f"""
            <div class="card">
              <div class="card-header">
                <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDetector{detector}" aria-expanded="false" aria-controls="collapseDetector{detector}">
                  {detector}
                </button>
              </div>
              <div id="collapseDetector{detector}" class="collapse" data-parent="#foldersList">
                <div class="card-body">
            """
            for version in os.listdir(detector_path):
                version_path = os.path.join(detector_path, version)
                if os.path.isdir(version_path):
                    main_html += f"""
                    <div class="card">
                      <div class="card-header">
                        <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#collapseVersion{detector}{version}" aria-expanded="false" aria-controls="collapseVersion{detector}{version}">
                          {version}
                        </button>
                      </div>
                      <div id="collapseVersion{detector}{version}" class="collapse" data-parent="#collapseDetector{detector}">
                        <div class="card-body">
                    """
                    for subsystem in os.listdir(version_path):
                        subsystem_path = os.path.join(version_path, subsystem)
                        if os.path.isdir(subsystem_path):
                            subsystem_link = f"{detector}/{version}/{subsystem}"
                            subsystem_output_dir = os.path.join(output_dir, subsystem_link)
                            plots = [os.path.join(subsystem_link, plot) for plot in os.listdir(subsystem_path) if plot.endswith('.svg')]
                            generate_subsystem_page(subsystem_path, plots, subsystem_output_dir)
                            main_html += f"""
                            <div class="card">
                              <div class="card-header">
                                <a class="btn btn-link" href="{subsystem_link}/index.html">
                                  {subsystem}
                                </a>
                              </div>
                            </div>
                            """
                    main_html += """
                        </div>
                      </div>
                    </div>
                    """
            main_html += """
                </div>
              </div>
            </div>
            """
    main_html += """
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
      </body>
    </html>
    """

    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(main_html)

if __name__ == "__main__":
    parent_directory = "../../scripts/FCCee"  # Replace with your parent directory
    output_directory = "../../scripts/FCCee"  # Replace with your desired output directory
    generate_main_page(parent_directory, output_directory)
