def create_config(custom_config):
    # Convert README.md to rst.

    f = open("README.md", mode = "rt", encoding = "utf-8")
    lines = []

    for line in f.readlines():
        underline = None

        if line.startswith("# "):
            line = line[2:]
            underline = "="
        elif line.startswith("## "):
            line = line[3:]
            underline = "-"

        lines.append(line)
        if underline != None:
            line = "{}\n".format((len(line) - 1) * underline)
            lines.append(line)

    f.close()
    long_description = "".join(lines)

    # Create distutils config.

    config = {"version": "0.0.4-dev",
              "long_description": long_description,
              "author": "Szalai András",
              "author_email": "andrew@bandipapa.com",
              "url": "https://github.com/bandipapa/MyRPC",
              "platforms": "cross-platform",
              "license": "BSD",
              "keywords": "rpc, Python, JavaScript, Node.js, cross-platform, framework",
              "classifiers": ["Development Status :: 4 - Beta",
                              "Intended Audience :: Developers",
                              "License :: OSI Approved :: BSD License",
                              "Operating System :: OS Independent",
                              "Programming Language :: Python :: 3.3",
                              "Topic :: Software Development :: Object Brokering"]}

    config.update(custom_config)

    return config
