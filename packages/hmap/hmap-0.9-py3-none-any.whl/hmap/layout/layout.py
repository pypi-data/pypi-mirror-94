from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt

def layoutGrid(nrows, ncols, row_widths, col_heights, hspace, wspace, bottom,
               top, left, right):
    '''
		Function, that makes a grid layout using extensions given in mm.

		args:
			nrows: int
				Number of rows in the grid.
			ncols: int
				Number of columns in the grid.
			row_withs: list<float>
				Widths of rows in mm.
			col_heights: list<float>
				Heights of columns in mm.
			hspace: float
				Height space between cells in mm.
			wspace: float
				Width space between cells in mm.
			bottom: float
				Bottom space of grid in mm.
			top: float
				Top space of grid in mm.
			left: float
				Left space of grid in mm.
			right: float
				Right space of grid in mm.

		Returns: tuple
			fig: matplotlib.pyplot.Figure
				Figure on which the grid is defined.
			gs: matplotlib.gridspec.GridSpec
				Layouted grid.
    '''
	# Define overall extensions of figure in mm
    overall_width = float(sum(row_widths)+float(ncols-1)*wspace+left+right)
    overall_height = float(sum(col_heights)+float(nrows-1)*hspace+bottom+top)

	# Declare figure width overall extensions in inches
    fig = plt.figure(figsize = (overall_width/25.4,
                                overall_height/25.4),
                     dpi=300)

	# Define fractions of left, right, bottom and top
    left_frac = left/overall_width
    right_frac = 1.-(right/overall_width)
    bottom_frac = bottom/overall_height
    top_frac = 1.-(top/overall_height)

	# Define fractions of row_widths, and col_heights
    row_widths_frac = [ w/overall_width for w in row_widths ]
    col_heights_frac = [ h/overall_height for h in col_heights ]
    average_row_widths_frac = sum(row_widths_frac)/float(len(row_widths_frac))
    average_col_heights_frac = (sum(col_heights_frac)/
                             float(len(col_heights_frac)))
    average_row_widths = average_row_widths_frac*overall_width
    average_col_heights = average_col_heights_frac*overall_height

	# Define fractions of wspace and hspace
    wspace_frac = (wspace)/(sum(row_widths)/float(len(row_widths)))
    hspace_frac = (hspace)/(sum(col_heights)/float(len(col_heights)))

	# Define GridSpec
    gs = GridSpec(ncols = ncols,
		nrows = nrows,
		width_ratios = row_widths_frac,
		height_ratios = col_heights_frac,
		hspace = hspace_frac,
		wspace = wspace_frac,
		bottom = bottom_frac,
		top = top_frac,
		left = left_frac,
		right = right_frac)

    return fig, gs
