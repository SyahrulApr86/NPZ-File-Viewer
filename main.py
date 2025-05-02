import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.cm as cm


class NPZViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("NPZ File Viewer")
        self.root.geometry("800x600")

        # Create frame for the main layout
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Add a button to open NPZ file
        self.btn_open = ttk.Button(self.main_frame, text="Buka File NPZ", command=self.open_npz_file)
        self.btn_open.pack(pady=10)

        # Label to show selected file
        self.lbl_file = ttk.Label(self.main_frame, text="File belum dipilih")
        self.lbl_file.pack(pady=5)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Siap")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Store the array tabs
        self.array_tabs = {}

    def open_npz_file(self):
        # Open file dialog to select an NPZ file
        file_path = filedialog.askopenfilename(
            title="Pilih File NPZ",
            filetypes=[("NPZ files", "*.npz"), ("All files", "*.*")]
        )

        if not file_path:
            return

        # Clear previous tabs
        for tab in self.array_tabs.values():
            tab.destroy()
        self.array_tabs = {}

        for i in range(self.notebook.index("end") - 1, -1, -1):
            self.notebook.forget(i)

        self.lbl_file.config(text=f"File: {os.path.basename(file_path)}")
        self.status_var.set(f"Membuka file: {file_path}")

        try:
            # Load the NPZ file
            with np.load(file_path) as npz_file:
                if not npz_file.files:
                    self.status_var.set("File NPZ kosong!")
                    return

                # Create a tab for each array in the NPZ file
                for name in npz_file.files:
                    array = npz_file[name]
                    self.create_array_tab(name, array)

                self.status_var.set(f"Berhasil memuat {len(npz_file.files)} array dari file NPZ")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            tk.messagebox.showerror("Error", f"Gagal membuka file NPZ:\n{str(e)}")

    def create_array_tab(self, name, array):
        # Create a tab for this array
        tab = ttk.Frame(self.notebook)
        self.array_tabs[name] = tab
        self.notebook.add(tab, text=name)

        # Handle scalar or empty arrays differently
        if array.size == 1 or array.shape == ():
            # For scalar values, just show the value directly
            self.create_scalar_tab(tab, name, array)
            return

        # Create a notebook inside the tab for "Data" and "Visualization" tabs
        inner_notebook = ttk.Notebook(tab)
        inner_notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Create Data Tab
        data_tab = ttk.Frame(inner_notebook)
        inner_notebook.add(data_tab, text="Data")

        # Create Visualization Tab
        viz_tab = ttk.Frame(inner_notebook)
        inner_notebook.add(viz_tab, text="Visualisasi")

        # Setup Data Tab
        # Create scrollable frame
        frame_canvas = ttk.Frame(data_tab)
        frame_canvas.pack(fill=tk.BOTH, expand=True)

        # Add a canvas with scrollbar
        canvas = tk.Canvas(frame_canvas)
        scrollbar_y = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Add array information
        ttk.Label(inner_frame, text=f"Name: {name}", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        ttk.Label(inner_frame, text=f"Shape: {array.shape}").pack(anchor="w")
        ttk.Label(inner_frame, text=f"Data Type: {array.dtype}").pack(anchor="w")

        # Add separator
        ttk.Separator(inner_frame, orient="horizontal").pack(fill="x", pady=10)

        # Show array data
        # For 1D and 2D arrays, show in a tabular format
        # For higher dimensions, just show statistics
        if array.ndim <= 2:
            self.display_array_data(inner_frame, array)
        else:
            self.display_array_stats(inner_frame, array)

        # Setup Visualization Tab
        self.visualize_array(viz_tab, name, array)

    def create_scalar_tab(self, tab, name, array):
        """Create a simplified tab for scalar values"""
        # Create frame for content
        main_frame = ttk.Frame(tab, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Add array information with larger font
        ttk.Label(main_frame, text=f"Name: {name}", font=("Arial", 14, "bold")).pack(anchor="w", pady=10)
        ttk.Label(main_frame, text=f"Shape: {array.shape}", font=("Arial", 12)).pack(anchor="w", pady=5)
        ttk.Label(main_frame, text=f"Data Type: {array.dtype}", font=("Arial", 12)).pack(anchor="w", pady=5)

        # Add separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=20)

        # Display the value prominently
        value_frame = ttk.Frame(main_frame)
        value_frame.pack(pady=30, fill="x")

        ttk.Label(value_frame, text="Nilai:", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        # Format the value display based on its type
        if np.issubdtype(array.dtype, np.integer):
            value_str = f"{array.item():,d}"
        elif np.issubdtype(array.dtype, np.floating):
            value_str = f"{array.item():.6g}"
        else:
            value_str = str(array.item())

        value_label = ttk.Label(value_frame, text=value_str, font=("Courier New", 16))
        value_label.pack(side="left", padx=20)

        # Add copy button
        copy_btn = ttk.Button(value_frame, text="Salin", command=lambda: self.copy_to_clipboard(value_str))
        copy_btn.pack(side="left", padx=10)

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set(f"Nilai telah disalin ke clipboard!")

        # Reset status after 2 seconds
        self.root.after(2000, lambda: self.status_var.set("Siap"))

    def display_array_data(self, parent, array):
        # Create a frame for the data
        data_frame = ttk.Frame(parent)
        data_frame.pack(fill="both", expand=True, pady=10)

        ttk.Label(parent, text="Array Data:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)

        # For 1D array
        if array.ndim == 1:
            # Create treeview for tabular display
            columns = min(20, len(array))
            tree = ttk.Treeview(data_frame, columns=tuple(range(columns)), show='headings', height=5)

            # Configure columns
            for i in range(columns):
                tree.heading(i, text=f"{i}")
                tree.column(i, width=50)

            # Insert data
            values = []
            for i in range(min(len(array), 20)):
                values.append(str(array[i]))

            if len(values) > 0:
                tree.insert('', 'end', values=values)

            tree.pack(fill="both", expand=True)

            if len(array) > 20:
                ttk.Label(data_frame, text=f"... (showing 20 of {len(array)} elements)").pack(anchor="w")

        # For 2D array
        elif array.ndim == 2:
            rows, cols = array.shape
            display_rows = min(20, rows)
            display_cols = min(20, cols)

            # Create treeview for tabular display
            tree = ttk.Treeview(data_frame, columns=tuple(range(display_cols)), show='headings',
                                height=min(10, display_rows))

            # Configure columns
            for i in range(display_cols):
                tree.heading(i, text=f"{i}")
                tree.column(i, width=50)

            # Insert data
            for i in range(display_rows):
                values = []
                for j in range(display_cols):
                    values.append(str(array[i, j]))
                tree.insert('', 'end', values=values)

            tree.pack(fill="both", expand=True)

            if rows > 20 or cols > 20:
                ttk.Label(data_frame,
                          text=f"... (showing {display_rows}x{display_cols} of {rows}x{cols} elements)").pack(
                    anchor="w")

    def display_array_stats(self, parent, array):
        ttk.Label(parent, text="Array Statistics (high-dimensional array):", font=("Arial", 10, "bold")).pack(
            anchor="w", pady=5)

        # Show statistics instead of raw data for high-dimensional arrays
        stats_text = f"""
        Dimensions: {array.ndim}
        Shape: {array.shape}
        Total Elements: {array.size}
        Memory Size: {array.nbytes / 1024:.2f} KB

        Min Value: {array.min()}
        Max Value: {array.max()}
        Mean: {array.mean()}
        Standard Deviation: {array.std()}
        """

        stats_label = ttk.Label(parent, text=stats_text, justify="left")
        stats_label.pack(anchor="w", pady=10)

    def visualize_array(self, parent, name, array):
        """Create visualization for the array based on its dimensionality"""
        # Control frame for visualization options
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill="x", pady=5)

        # Create a figure for matplotlib
        fig_frame = ttk.Frame(parent)
        fig_frame.pack(fill="both", expand=True, pady=5)

        fig = Figure(figsize=(8, 6), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Handle different dimensionality for visualization
        if array.ndim == 1:
            self.visualize_1d_array(fig, control_frame, array, canvas)
        elif array.ndim == 2:
            self.visualize_2d_array(fig, control_frame, array, canvas)
        else:
            self.visualize_nd_array(fig, control_frame, array, canvas)

    def visualize_1d_array(self, fig, control_frame, array, canvas):
        """Visualize 1D array with line plot, histogram, etc."""
        # Create visualization type selector
        ttk.Label(control_frame, text="Tipe Visualisasi:").pack(side="left", padx=5)
        viz_type = tk.StringVar(value="line")

        def update_viz(*args):
            fig.clear()
            ax = fig.add_subplot(111)

            if viz_type.get() == "line":
                ax.plot(array, '-o')
                ax.set_title("Line Plot")
                ax.set_xlabel("Index")
                ax.set_ylabel("Value")

            elif viz_type.get() == "hist":
                ax.hist(array, bins=min(50, max(10, array.size // 10)), alpha=0.7)
                ax.set_title("Histogram")
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")

            elif viz_type.get() == "bar":
                if array.size <= 100:  # Only show bar for reasonable number of elements
                    ax.bar(range(array.size), array)
                    ax.set_title("Bar Plot")
                    ax.set_xlabel("Index")
                    ax.set_ylabel("Value")
                else:
                    ax.text(0.5, 0.5, "Too many elements for bar plot",
                            ha='center', va='center', transform=ax.transAxes)

            fig.tight_layout()
            canvas.draw()

        viz_options = ttk.Combobox(control_frame, textvariable=viz_type,
                                   values=["line", "hist", "bar"])
        viz_options.pack(side="left", padx=5)
        viz_options.bind("<<ComboboxSelected>>", update_viz)

        # Initial visualization
        update_viz()

    def visualize_2d_array(self, fig, control_frame, array, canvas):
        """Visualize 2D array with heatmap, surface plot, etc."""
        ttk.Label(control_frame, text="Tipe Visualisasi:").pack(side="left", padx=5)

        # Determine available visualization types based on array shape
        if array.shape[1] == 3:  # Special case for (n, 3) arrays
            viz_types = ["heatmap", "contour", "wireframe", "columns_plot", "3d_scatter"]
            default_viz = "columns_plot"
        else:
            viz_types = ["heatmap", "contour", "wireframe"]
            default_viz = "heatmap"

        viz_type = tk.StringVar(value=default_viz)

        # Colormap selector
        ttk.Label(control_frame, text="Colormap:").pack(side="left", padx=5)
        cmap_var = tk.StringVar(value="viridis")
        cmaps = ["viridis", "plasma", "inferno", "magma", "cividis", "hot", "cool", "jet"]

        # Add control for 3D scatter if shape is (n, 3)
        col_labels = ["X", "Y", "Z"]
        col_mapping = {}

        if array.shape[1] == 3:
            # Frame for column mapping controls
            col_frame = ttk.LabelFrame(control_frame, text="Column Mapping")
            col_frame.pack(side="left", padx=10, fill="y")

            for i in range(3):
                var = tk.IntVar(value=i)
                col_mapping[i] = var

                # Only show these controls for 3d_scatter
                frame = ttk.Frame(col_frame)
                frame.pack(fill="x", pady=2)
                ttk.Label(frame, text=f"{col_labels[i]} Axis:").pack(side="left")
                col_dropdown = ttk.Combobox(frame, textvariable=var, values=[0, 1, 2], width=2)
                col_dropdown.pack(side="left", padx=5)

        def update_viz(*args):
            fig.clear()

            if viz_type.get() == "heatmap":
                ax = fig.add_subplot(111)
                # Check if array dimensions are too large for display
                if array.shape[0] > 1000 or array.shape[1] > 1000:
                    # Sample the array for display
                    step_y = max(1, array.shape[0] // 1000)
                    step_x = max(1, array.shape[1] // 1000)
                    display_array = array[::step_y, ::step_x]
                    ax.set_title(f"Heatmap (Sampled 1:{step_y}x{step_x})")
                else:
                    display_array = array
                    ax.set_title("Heatmap")

                im = ax.imshow(display_array, cmap=cmap_var.get(), aspect='auto')
                fig.colorbar(im, ax=ax)

            elif viz_type.get() == "contour":
                ax = fig.add_subplot(111)
                if array.shape[0] > 500 or array.shape[1] > 500:
                    step_y = max(1, array.shape[0] // 500)
                    step_x = max(1, array.shape[1] // 500)
                    display_array = array[::step_y, ::step_x]
                    ax.set_title(f"Contour Plot (Sampled 1:{step_y}x{step_x})")
                else:
                    display_array = array
                    ax.set_title("Contour Plot")

                # Create grid for contour plot
                y, x = np.mgrid[:display_array.shape[0], :display_array.shape[1]]
                cs = ax.contourf(x, y, display_array, cmap=cmap_var.get())
                fig.colorbar(cs, ax=ax)

            elif viz_type.get() == "wireframe":
                # Convert to 3D plot for wireframe
                if array.shape[0] > 100 or array.shape[1] > 100:
                    step_y = max(1, array.shape[0] // 100)
                    step_x = max(1, array.shape[1] // 100)
                    display_array = array[::step_y, ::step_x]
                    title = f"Wireframe (Sampled 1:{step_y}x{step_x})"
                else:
                    display_array = array
                    title = "Wireframe"

                ax = fig.add_subplot(111, projection='3d')
                y, x = np.mgrid[:display_array.shape[0], :display_array.shape[1]]
                ax.plot_wireframe(x, y, display_array, rstride=1, cstride=1, color='blue')
                ax.set_title(title)

            elif viz_type.get() == "columns_plot" and array.shape[1] == 3:
                # Plot each column as a separate line in one subplot
                ax1 = fig.add_subplot(311)
                ax2 = fig.add_subplot(312)
                ax3 = fig.add_subplot(313)

                axes = [ax1, ax2, ax3]

                # Plot each column
                for i in range(3):
                    axes[i].plot(array[:, i], label=f"Column {i}")
                    axes[i].set_title(f"Column {i} Values")
                    axes[i].set_xlabel("Index")
                    axes[i].set_ylabel("Value")
                    axes[i].grid(True)

                fig.tight_layout()

            elif viz_type.get() == "3d_scatter" and array.shape[1] == 3:
                # 3D scatter plot for (n, 3) data
                ax = fig.add_subplot(111, projection='3d')

                # Get column mapping
                x_col = col_mapping[0].get()
                y_col = col_mapping[1].get()
                z_col = col_mapping[2].get()

                # Sample data if it's too large
                if array.shape[0] > 5000:
                    step = max(1, array.shape[0] // 5000)
                    display_array = array[::step, :]
                    title = f"3D Scatter (Sampled 1:{step})"
                else:
                    display_array = array
                    title = "3D Scatter"

                # Create 3D scatter plot
                ax.scatter(
                    display_array[:, x_col],
                    display_array[:, y_col],
                    display_array[:, z_col],
                    c=np.arange(len(display_array)),
                    cmap=cmap_var.get(),
                    marker='.',
                    alpha=0.7
                )

                ax.set_xlabel(f"Column {x_col}")
                ax.set_ylabel(f"Column {y_col}")
                ax.set_zlabel(f"Column {z_col}")
                ax.set_title(title)

            # Refresh canvas
            fig.tight_layout()
            canvas.draw()

            # Show/hide column mapping controls based on viz type
            if array.shape[1] == 3:
                if viz_type.get() == "3d_scatter":
                    col_frame.pack(side="left", padx=10, fill="y")
                else:
                    col_frame.pack_forget()

        viz_options = ttk.Combobox(control_frame, textvariable=viz_type, values=viz_types)
        viz_options.pack(side="left", padx=5)
        viz_options.bind("<<ComboboxSelected>>", update_viz)

        cmap_options = ttk.Combobox(control_frame, textvariable=cmap_var, values=cmaps)
        cmap_options.pack(side="left", padx=5)
        cmap_options.bind("<<ComboboxSelected>>", update_viz)

        # Initial visualization
        update_viz()

    def visualize_nd_array(self, fig, control_frame, array, canvas):
        """Visualize higher dimensional arrays with projections, histograms, etc."""
        ttk.Label(control_frame, text="Tipe Visualisasi:").pack(side="left", padx=5)
        viz_type = tk.StringVar(value="histogram")

        # For 3D+ arrays, allow selection of slices or projections
        dim_frame = ttk.Frame(control_frame)
        dim_frame.pack(side="left", padx=10)

        # Variables to hold slice information
        slice_vars = []
        slice_entries = []
        max_dims_to_show = min(3, array.ndim)

        def update_viz(*args):
            fig.clear()

            if viz_type.get() == "histogram":
                # Flattened histogram of all values
                ax = fig.add_subplot(111)
                ax.hist(array.flatten(), bins=50, alpha=0.7)
                ax.set_title("Histogram of All Values")
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")

            elif viz_type.get() == "slice":
                # Extract slice indices from entries
                try:
                    indices = []
                    for i, var in enumerate(slice_vars):
                        if i < array.ndim:
                            val = var.get()
                            if val == "":
                                indices.append(slice(None))
                            else:
                                indices.append(int(val))

                    # Get the slice
                    slice_array = array[tuple(indices)]

                    # Plot based on dimensionality of the resulting slice
                    if slice_array.ndim == 1:
                        ax = fig.add_subplot(111)
                        ax.plot(slice_array)
                        ax.set_title(f"1D Slice at {indices}")
                        ax.set_xlabel("Index")
                        ax.set_ylabel("Value")
                    elif slice_array.ndim == 2:
                        ax = fig.add_subplot(111)
                        im = ax.imshow(slice_array, aspect='auto')
                        fig.colorbar(im, ax=ax)
                        ax.set_title(f"2D Slice at {indices}")
                    else:
                        ax = fig.add_subplot(111)
                        ax.text(0.5, 0.5,
                                f"Slice has {slice_array.ndim} dimensions\nUse more indices to get 1D or 2D view",
                                ha='center', va='center')
                except Exception as e:
                    ax = fig.add_subplot(111)
                    ax.text(0.5, 0.5, f"Error creating slice: {str(e)}", ha='center', va='center')

            fig.tight_layout()
            canvas.draw()

        def setup_slice_controls():
            # Clear existing controls
            for widget in dim_frame.winfo_children():
                widget.destroy()

            slice_vars.clear()
            slice_entries.clear()

            if viz_type.get() == "slice":
                # Create inputs for each dimension (up to 3 for simplicity)
                ttk.Label(dim_frame, text="Enter slice indices (empty for ':')").pack(anchor="w")

                for i in range(min(array.ndim, max_dims_to_show)):
                    frame = ttk.Frame(dim_frame)
                    frame.pack(fill="x", pady=2)

                    ttk.Label(frame, text=f"Dim {i} (0-{array.shape[i] - 1}):").pack(side="left")
                    var = tk.StringVar()
                    slice_vars.append(var)

                    entry = ttk.Entry(frame, textvariable=var, width=8)
                    entry.pack(side="left", padx=5)
                    slice_entries.append(entry)

                    var.trace("w", update_viz)

                if array.ndim > max_dims_to_show:
                    ttk.Label(dim_frame, text=f"+ {array.ndim - max_dims_to_show} more dimensions").pack(anchor="w")

                # Add "Update" button
                ttk.Button(dim_frame, text="Update", command=update_viz).pack(pady=5)

        def on_viz_type_change(*args):
            setup_slice_controls()
            update_viz()

        viz_options = ttk.Combobox(control_frame, textvariable=viz_type,
                                   values=["histogram", "slice"])
        viz_options.pack(side="left", padx=5)
        viz_options.bind("<<ComboboxSelected>>", on_viz_type_change)

        # Initial setup
        setup_slice_controls()
        update_viz()


def main():
    root = tk.Tk()
    app = NPZViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()