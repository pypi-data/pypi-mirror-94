## TaXon table filtering
#1.a create mask for user input
def create_taxa_mask(TaXon_table_xlsx, mask, taxon_mask):

    import pandas as pd
    from pandas import DataFrame
    from pathlib import Path

    TaXon_table_xlsx = Path(TaXon_table_xlsx)
    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_xlsx)
    data = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)

    available_taxa = set(data[mask].values.tolist())
    available_taxa = [x for x in available_taxa if str(x) != 'nan']
    available_taxa = sorted(list(available_taxa))

    if taxon_mask != "":
        available_taxa = [taxon for taxon in available_taxa if taxon_mask in taxon]

    return available_taxa

# 1.b filter taxa from taxon table
def taxon_filter(TaXon_table_xlsx, filtered_taxa, mask, appendix_name, threshold, path_to_outdirs, taxon_filter_method):

    import PySimpleGUI as sg
    import pandas as pd
    from pandas import DataFrame
    from pathlib import Path

    TaXon_table_file =  Path(TaXon_table_xlsx)

    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_file)
    df = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)
    # convert taxa to exclude to a list if only one taxon is given (which is then string)
    if type(filtered_taxa) == str:
        filtered_taxa = [filtered_taxa]

    if taxon_filter_method == "keep":
        available_taxa = set(df[mask].values.tolist())
        available_taxa = [x for x in available_taxa if str(x) != 'nan']
        available_taxa = sorted(list(available_taxa))
        filtered_taxa = list(set(available_taxa) - set(filtered_taxa))

    # check for taxa to filter
    mask_position = list(df.columns).index(mask)
    df_columns = df.columns

    rows_to_keep = []

    df_rows = df.values.tolist()
    for row in df_rows:
        taxon_to_evaluate = row[mask_position]
        if taxon_to_evaluate not in filtered_taxa:
            if str(taxon_to_evaluate) != 'nan':
                rows_to_keep.append(row)

    df_out = pd.DataFrame(rows_to_keep)

    similarity_position = list(df_columns).index("Similarity")
    threshold = int(threshold)

    filtered_rows = []

    for index, row in df_out.iterrows():
        similarity = list(row)[similarity_position]
        if similarity != 'No Match':
            if int(similarity) >= threshold:
                filtered_rows.append(list(row))

    df_out = pd.DataFrame(filtered_rows)

    if df_out.empty:
        sg.PopupError('Filter theshold were to harsh: Nothing to print', title="Error", keep_on_top=True)

    else:
        df_out.columns = df_columns

        # write output file
        file_name = TaXon_table_file.stem
        output_name = Path(str(path_to_outdirs) + "/" + "TaXon_tables" + "/" + file_name + "_" + appendix_name + ".xlsx")
        threshold_output = "Similarity threshold = " + str(threshold)
        filtered_taxa.append(threshold_output)
        df_filtered_taxa = pd.DataFrame(filtered_taxa)
        df_filtered_taxa.columns = ['Filter criteria']
        writer = pd.ExcelWriter(output_name, engine = 'xlsxwriter')
        df_out.to_excel(writer, sheet_name = 'TaXon table', index=False)
        df_filtered_taxa.to_excel(writer, sheet_name = 'Filter criteria', index=False)
        writer.save()
        writer.close()

        closing_text = "Taxon table is found under:\n" + '/'.join(str(output_name).split("/")[-4:])
        sg.Popup(closing_text, title="Finished", keep_on_top=True)

        from taxontabletools.create_log import ttt_log
        ttt_log("taxon filter", "processing", TaXon_table_file.name, output_name.name, "nan", path_to_outdirs)

# 2.a create mask for user input
def create_sample_mask(TaXon_table_xlsx, sample_mask):

    import pandas as pd
    from pandas import DataFrame
    from pathlib import Path

    TaXon_table_xlsx = Path(TaXon_table_xlsx)
    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_xlsx)
    df = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)

    available_samples = df.columns.tolist()[10:]

    if sample_mask != "":
        available_samples = [sample for sample in available_samples if sample_mask in sample]

    return available_samples

# 2.b filter samples from taxon list
def filter_samples(TaXon_table_xlsx, selected_samples, appendix_name, path_to_outdirs, sample_filter_method):

    import PySimpleGUI as sg
    import pandas as pd
    from pandas import DataFrame
    from pathlib import Path

    TaXon_table_file =  Path(TaXon_table_xlsx)

    TaXon_table_xlsx_path = TaXon_table_xlsx
    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_xlsx)
    df = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)

    if type(selected_samples) == str:
        selected_samples = [selected_samples]

    if sample_filter_method == "exclude":
        for sample in selected_samples:
            df = df.drop(sample, axis=1)
    else:
        available_samples = df.columns.tolist()[10:]
        for sample in available_samples:
            if sample not in selected_samples:
                df = df.drop(sample, axis=1)

    header = df.columns.values.tolist()

    row_filter_list = []

    for row in df.values.tolist():
        reads = set(row[10:])
        if reads != {0}:
            row_filter_list.append(row)

    df = pd.DataFrame(row_filter_list)
    df.columns = header

    file_name = TaXon_table_file.stem
    output_name = Path(str(path_to_outdirs) + "/" + "TaXon_tables" + "/" + file_name + "_" + appendix_name + ".xlsx")
    df.to_excel(output_name, sheet_name = 'TaXon table', index=False)

    closing_text = "Taxon table is found under:\n" + '/'.join(str(output_name).split("/")[-4:])
    sg.Popup(closing_text, title="Finished", keep_on_top=True)

    from taxontabletools.create_log import ttt_log
    ttt_log("sample filter", "processing", TaXon_table_file.name, output_name.name, "nan", path_to_outdirs)

# 3 read-based filter
def read_filter(TaXon_table_xlsx, path_to_outdirs, read_filter_method, read_filter_treshold):
    import PySimpleGUI as sg
    import pandas as pd
    from pandas import DataFrame
    from pathlib import Path
    import numpy as np

    TaXon_table_file =  Path(TaXon_table_xlsx)
    TaXon_table_xlsx_path = TaXon_table_xlsx
    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_xlsx)
    TaXon_table_df = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)
    samples = TaXon_table_df.columns.tolist()[10:]

    if read_filter_method == "absolute_filtering":

        ## transform dataframe to array and apply filter threshold
        a = np.array(TaXon_table_df[samples].values.tolist())
        TaXon_table_df[samples] = np.where(a < int(read_filter_treshold), 0, a).tolist()

        ## remove OTUs that have 0 reads after filtering
        row_filter_list = []
        for row in TaXon_table_df.values.tolist():
            reads = set(row[10:])
            if reads != {0}:
                row_filter_list.append(row)
        TaXon_table_df_filtered = pd.DataFrame(row_filter_list)
        TaXon_table_df_filtered.columns = TaXon_table_df.columns.tolist()

        ## save filtered dataframe to file
        file_name = TaXon_table_file.stem
        output_name = Path(str(path_to_outdirs) + "/TaXon_tables/" + file_name + "_" + read_filter_treshold + ".xlsx")
        TaXon_table_df_filtered.to_excel(output_name, sheet_name = 'TaXon table', index=False)

        ## finish script
        closing_text = "Taxon table is found under:\n" + '/'.join(str(output_name).split("/")[-4:])
        sg.Popup(closing_text, title="Finished", keep_on_top=True)

        from taxontabletools.create_log import ttt_log
        ttt_log("absolute read filter", "processing", TaXon_table_file.name, output_name.name, read_filter_treshold, path_to_outdirs)

    elif read_filter_method == "relative_filtering":
        ## transform to percentage
        read_filter_rel = float(read_filter_treshold) / 100
        for sample in samples:
            ## transform to array
            a = np.array(TaXon_table_df[sample].values.tolist())
            ## calculate threshold for each sample
            sample_threshold = sum(a) * read_filter_rel
            ## apply filter to dataframe
            TaXon_table_df[sample] = np.where(a < int(sample_threshold), 0, a).tolist()

        ## remove OTUs that have 0 reads after filtering
        row_filter_list = []
        for row in TaXon_table_df.values.tolist():
            reads = set(row[10:])
            if reads != {0}:
                row_filter_list.append(row)
        TaXon_table_df_filtered = pd.DataFrame(row_filter_list)
        TaXon_table_df_filtered.columns = TaXon_table_df.columns.tolist()

        ## save filtered dataframe to file
        file_name = TaXon_table_file.stem
        output_name = Path(str(path_to_outdirs) + "/TaXon_tables/" + file_name + "_" + read_filter_treshold + ".xlsx")
        TaXon_table_df_filtered.to_excel(output_name, sheet_name = 'TaXon table', index=False)

        ## finish script
        closing_text = "Taxon table is found under:\n" + '/'.join(str(output_name).split("/")[-4:])
        sg.Popup(closing_text, title="Finished", keep_on_top=True)

        from taxontabletools.create_log import ttt_log
        ttt_log("relative read filter", "processing", TaXon_table_file.name, output_name.name, read_filter_treshold, path_to_outdirs)




#
