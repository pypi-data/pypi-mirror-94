from cygnsslib.CygDdmId import CygDdmId
import os
import xlrd
import xlwt


def find_land_prod_sample_id_from_excel(xls_in, xls_out=None, start_col=1, st_row=1, out_sheet_suffix='', land_samp_col=None, timestamp_col=None):
    """

    Read the first sheet and the col. start_col to start_col+4.

    The output file is all the cells with new column: land_sample_zero_based

    :param xls_in: input Excel file
    :type xls_in: str
    :param xls_out: output Excel file name, if None add "_land_prod" to the file
    :type xls_out: str or None
    :param start_col: starting col. the function read start_col to start_col+4
    :type start_col: int
    :param st_row: Starting row, default 1 which is the header
    :type st_row: int
    :param out_sheet_suffix: suffix of the sheet name (NOT file name)
    :type out_sheet_suffix: str
    :param land_samp_col: col number of land_sample_zero_based, if None the default is start_col + 5
    :type land_samp_col: int or None
    :param timestamp_col: write the timestamp to tis col. if None the function will not write the timestamp
    :type timestamp_col: int or None
    :return: output file name
    :rtype: str
    """
    if xls_out is None:
        inxls_list = xls_in.split('.')
        xls_out = '{:s}_land_prod.{:s}'.format(inxls_list[0], 'xls')  # car read xlsx and xls but write only to xls

    if not os.path.exists(xls_in):
        raise FileExistsError("Input Excel file doesn't exist, {:s}".format(xls_in))

    wd = xlrd.open_workbook(xls_in, on_demand=True)
    in_sheet = wd.sheet_by_index(0)

    if land_samp_col is None or land_samp_col < 0:
        land_samp_col = start_col + 5

    year_col = in_sheet.col_values(start_col, start_rowx=st_row)
    day_col = in_sheet.col_values(start_col+1, start_rowx=st_row)
    sc_num_col = in_sheet.col_values(start_col+2, start_rowx=st_row)
    ch_id_col = in_sheet.col_values(start_col+3, start_rowx=st_row)
    ocean_sample_col = in_sheet.col_values(start_col+4, start_rowx=st_row)

    list_ddm_id = list()
    for row in range(len(year_col)):
        list_ddm_id.append(CygDdmId(None, year_col[row], day_col[row], sc_num_col[row], ch_id_col[row], ocean_sample_col[row]))
        list_ddm_id[row].fill_land_parameters()

    col_header = in_sheet.row_values(0)
    col_header[start_col+4] = 'ocean_{:s}'.format(col_header[start_col+4])  # change sample number name to ocean ...
    col_header.append('land_sample_zero_based')
    workbook = xlwt.Workbook()
    out_sheet = workbook.add_sheet('{:s}{:s}'.format(in_sheet.name, out_sheet_suffix))
    # copy the original Excel file
    for col in range(in_sheet.ncols+1):
        if col < land_samp_col:
            out_sheet.write(0, col, col_header[col])
            for row in range(1, in_sheet.nrows):
                out_sheet.write(row, col, in_sheet.cell_value(row, col))
        elif col == land_samp_col:
            out_sheet.write(0, col, col_header[in_sheet.ncols])
            for row in range(st_row, in_sheet.nrows):
                out_sheet.write(row, col, list_ddm_id[row-st_row].land_samp_id)
        else:  # col > lamd_samp_col
            out_sheet.write(0, col, col_header[col-1])
            for row in range(1, in_sheet.nrows):
                out_sheet.write(row, col, in_sheet.cell_value(row, col-1))

    if timestamp_col is not None:
        for row in range(st_row, in_sheet.nrows):
            out_sheet._cell_overwrite_ok = True
            ddm_utc_time = list_ddm_id[row-st_row].get_utc_time()
            out_sheet.write(row, timestamp_col, ddm_utc_time.isoformat())

    workbook.save(xls_out)


if __name__ == '__main__':
    xls_in = 'SLV_Z4_thawed_2019.xlsx'
    find_land_prod_sample_id_from_excel(xls_in, xls_out=None, start_col=1, out_sheet_suffix='', timestamp_col=0)
    xls_in = 'SLV_Z1_thawed_2019.xlsx'
    find_land_prod_sample_id_from_excel(xls_in, xls_out=None, st_row=1, start_col=1, out_sheet_suffix='', timestamp_col=0)
