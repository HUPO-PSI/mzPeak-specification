import subprocess
import sys
import time


def main():
    # Read the mkdocs config
    with open('mkdocs.yml', 'rt') as fh:
        config = fh.read()

    # Remove the root `index.md` which is not appropriate for a specification
    # document. The modified config is rebuilt which takes ~10 seconds
    config = config.replace("- Home: index.md", '')
    server = subprocess.Popen([
        sys.executable,
        '-m',
        'mkdocs',
        'serve',
        '-f',
        '-',
    ], stdin=subprocess.PIPE)

    # Write the modified config into the `mkdocs` STDIN which `-f -` signals
    # is where the config YAML will be read from
    server.stdin.write(config.encode('utf8'))
    server.stdin.close()

    # Wait for the build process to finish
    time.sleep(20)

    # Run the automated PDF export through Puppeteer printing
    subprocess.check_call([
        "node",
        "scripts/export_to_pdf.js",
        "http://localhost:8000/mzPeak-specification/print_page/",
        "mzPeak-specification.pdf",
        'mzPeak'
    ])

    # Terminate the server process
    server.kill()

if __name__ == '__main__':
    main()
