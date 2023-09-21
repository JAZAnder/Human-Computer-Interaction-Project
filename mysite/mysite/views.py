from django.shortcuts import render
import mne
import os
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.tools import mpl_to_plotly


def landing_view(request):
    return render(request, "upload.html")


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        temp_file_path = "raw.fif"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Load the .fif file using MNE-Python
        raw = mne.io.read_raw_fif(temp_file_path)

        # Process the data and generate your MNE graph (replace this with your specific MNE graph generation code)
        # Example: Create a simple topographic plot
        layout = go.Layout(title='Simple MNE Plot')


        data = [go.Scatter(x=[1, 2, 3, 4, 5], y=[10, 11, 12, 13, 14], mode='lines')]

        # Generate an HTML representation of the Plotly graph
        plot_div = plot({'data': data, 'layout': layout}, output_type='div', include_plotlyjs=True)

        # Remove the temporary file
        os.remove(temp_file_path)

        return render(request, 'graph.html', {'plot_div': plot_div})
    return render(request, 'upload.html')