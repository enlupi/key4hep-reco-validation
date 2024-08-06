import os
import argparse
import jinja2
import datetime
from collections import defaultdict
import yaml

def get_latest_modified_date(folder_path):
    latest_modified_date = None

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_date = os.path.getmtime(file_path)

            if latest_modified_date is None or modified_date > latest_modified_date:
                latest_modified_date = modified_date

    if latest_modified_date is None:
        latest_modified_date = 0
    latest_modified_date = datetime.datetime.fromtimestamp(int(latest_modified_date))
    return latest_modified_date

def write_plots(folder):
    # Generate a list of the PNG images in the folder
    svg_files = [os.path.join('plots', filename) for filename in os.listdir(os.path.join(folder, 'plots')) if filename.endswith('.svg')]
    print(svg_files)

    # Generate the HTML markup using a Jinja2 template
    template = jinja2.Template('''
    {% for filename in svg_files %} <img src="{{ filename }}" class="plot-container"/>
    {% endfor %}
    ''')
    html = template.render(svg_files=svg_files)

    return html

def generate_subsystem_page(version_path, plots):
    version_name = os.path.basename(version_path)
    plot_html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{version_name}</title>
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
          <h1>{version_name}</h1>
          <div class="row">
    """
    for plot in plots:
        plot_html += f"""
            <div class="col-md-4">
              <img src="{plot}" class="img-fluid" alt="{plot}">
            </div>
        """
    plot_html += """
          </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
      </body>
    </html>
    """

    with open(os.path.join(version_path, "index.html"), "w") as f:
        f.write(plot_html)


def generate_main_page(dest):
    detector_folders = [folder for folder in os.listdir(dest) if os.path.isdir(os.path.join(dest, folder))]
    detector_folders.remove('static')

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

    for detector in detector_folders:
        detector_path = os.path.join(dest, detector)
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
            '''
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
                    '''
            
            #latest_modified_date = [get_latest_modified_date(os.path.join(detector_path, folder)) for folder in detector_path]
            for version in os.listdir(detector_path):
                version_path = os.path.join(detector_path, version)
                if os.path.isdir(version_path):
                  plots = [os.path.join(version_path, plot) for plot in os.listdir(version_path) if plot.endswith('.svg')]
                  generate_subsystem_page(version_path, plots)
                  main_html += f"""
                  <div class="card">
                    <div class="card-header">
                      <a class="btn btn-link" href="{version_path}/index.html">
                      {version}
                      </a>
                    </div>
                  </div>
                """
                main_html += """
                        </div>
                      </div>
                    </div>
                    """
            '''
            main_html += """
                </div>
              </div>
            </div>
            """
            '''
    main_html += """
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
      </body>
    </html>
    """

    with open(os.path.join(dest, "index.html"), "w") as f:
        f.write(main_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make the web pages for the validation website')
    parser.add_argument('--dest', required=True, help='Destination directory for the web pages', default='.')

    print("I AM RUNNING THE STUPID SCRIPT")

    args = parser.parse_args()
    generate_main_page(args.dest)