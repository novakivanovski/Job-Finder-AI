from Site import Site


def run():
    Site.app.run(debug=True)


@Site.app.route('/sandbox')
def sandbox():
    return 'Sandbox'
