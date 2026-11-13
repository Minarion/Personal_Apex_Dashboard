# Inbuilt
import requests

# Third Party
import dash

# Local
import dashboard_architecture

@dash.callback(
    dash.Output("tab_contents", "children"),
    dash.Input("tabs", "value"),
    suppress_callback_exceptions=True,
)
def tab_contents(tab_name):
    return dashboard_architecture.architecture["tabs"][tab_name]

@dash.callback(
    dash.Output("legend_stats", "children"),
    dash.Output("legend_icon", "src"),
    dash.Input("legend_selection", "value"),
    suppress_callback_exceptions=True,
)
def change_legend_image(legend_name):
    image_link = dashboard_architecture.test_data["legends"]["all"][legend_name]["ImgAssets"]["icon"]
    if requests.get(image_link).status_code == 404:
        image_link = "assets/image_not_found.jpg"

    try:
        legend_stats = [
            dash.html.Div(f"{subdict['name']}: {subdict['value']}")
            for subdict
            in dashboard_architecture.test_data["legends"]["all"][legend_name]["data"]
        ]
    except KeyError:
        legend_stats = []

    return legend_stats, image_link

if __name__ == '__main__':
    dashboard_architecture.app.run(debug=True)