# NPZ File Viewer

A Python-based graphical user interface (GUI) application for viewing and visualizing NumPy NPZ files. This tool allows you to explore the contents of NPZ files, view array data in tabular format, and visualize arrays with various plotting options.

## Features

- **File Browser**: Open and browse NPZ files through a simple file dialog
- **Multi-Array Support**: View all arrays contained within an NPZ file via a tabbed interface
- **Data Exploration**: Examine array metadata (shape, data type) and contents
- **Interactive Visualizations**: Visualize array data with multiple plot types
- **Specialized Data Handling**:
  - **Scalar Arrays**: Display single values with clean formatting and copy-to-clipboard functionality
  - **1D Arrays**: Line plots, histograms, and bar charts
  - **2D Arrays**: Heatmaps, contour plots, and 3D wireframes
  - **Shape (n, 3) Arrays**: Column plots and 3D scatter plots with customizable axis mapping
  - **Multi-dimensional Arrays**: Statistical summaries and slice viewer

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- Tkinter (usually comes with Python installation)

## Usage Guide

### Opening an NPZ File

1. Launch the application
2. Click the "Buka File NPZ" (Open NPZ File) button
3. Select an NPZ file from the file dialog
4. The application will load and display the contents of the file

### Navigating the Interface

- **Tabs**: Each array in the NPZ file is displayed in a separate tab labeled with its name
- **Data/Visualization Tabs**: For each array, you can switch between "Data" view and "Visualisasi" (Visualization) view
- **Status Bar**: Displays current application status and messages

### Data View

- Shows array metadata (name, shape, data type)
- For 1D and 2D arrays: Displays data in a tabular format (limited to first 20 rows/columns for large arrays)
- For multi-dimensional arrays: Displays statistical summary (min, max, mean, standard deviation)
- For scalar values: Displays the value prominently with a copy button

### Visualization View

The visualization options depend on the array dimensions:

#### For Scalar Arrays
- Direct value display with copy-to-clipboard functionality

#### For 1D Arrays
- **Line Plot**: Visualizes values against their indices
- **Histogram**: Shows the distribution of values
- **Bar Plot**: Displays values as bars (for smaller arrays)

#### For 2D Arrays
- **Heatmap**: Color-coded representation of the matrix
- **Contour Plot**: Topographical-style visualization
- **Wireframe**: 3D surface representation

#### For Shape (n, 3) Arrays
- **Columns Plot**: Three separate plots, one for each column
- **3D Scatter**: Points in 3D space with customizable axis mapping

#### For Multi-dimensional Arrays
- **Histogram**: Distribution of all values
- **Slice Viewer**: Interactive tool to view 2D slices of higher-dimensional data

## Examples

### Visualizing Time Series Data
If your NPZ file contains 1D arrays representing time series, use the "Line Plot" visualization to observe trends over time.

### Visualizing Image Data
For 2D arrays representing images, use the "Heatmap" visualization with different colormaps to enhance various features.

### Visualizing 3D Coordinates
For arrays with shape (n, 3) representing 3D coordinates, use the "3D Scatter" visualization to view the points in 3D space.

## Troubleshooting

### Common Issues

- **Memory Error**: When opening very large NPZ files, you may encounter memory limitations. The application attempts to handle this by sampling large arrays.
- **Display Issues**: For arrays with extreme values, visualizations may not render optimally. Try different visualization types.

### Performance Tips

- For large arrays, the application automatically samples data for visualization
- Close unused tabs to free up memory

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NumPy for the powerful array functionality
- Matplotlib for visualization capabilities
- Tkinter for the GUI framework