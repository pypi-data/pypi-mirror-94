import React, { Fragment, useEffect, useState } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';
import { MitoAPI } from '../../api';

/*
    A modal that allows a user to download their current sheet.

    It does this by:
    1. Getting a string representation of the sheet through the api
    2. Encoding that as a file
    3. Allowing the user to download that file

    To see more about this process, read documentation here: 
    https://blog.logrocket.com/programmatic-file-downloads-in-the-browser-9a5186298d5c/
*/
const DownloadModal = (
    props: {
        setModal: (modalInfo: ModalInfo) => void;
        mitoAPI: MitoAPI,
        selectedSheetIndex: number,
        dfName: string
    }): JSX.Element => {
    const [dataframeCSV, setDataframeCSV] = useState<string>('');

    const loadDataframeCSV = async () => {
        const loadedDataframeCSV = await props.mitoAPI.getDataframeAsCSV(props.selectedSheetIndex);
        setDataframeCSV(loadedDataframeCSV);
    }

    // Async load in the data from the mitoAPI
    useEffect(() => {
        void loadDataframeCSV()
    }, [])

    const onDownload = () => {
        void props.mitoAPI.sendLogMessage(
            'button_download_log_event',
            {
                sheet_index: props.selectedSheetIndex,
                df_name: props.dfName
            }
        )
        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
            header='Download Current Sheet'
            modalType={ModalEnum.Download}
            viewComponent= {
                <Fragment>
                    <p>
                        Download {props.dfName} as a CSV. 
                    </p>
                </Fragment>
            }
            buttons={
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    {/* 
                        Given the dataframe as a string, this encodes this string as a Blob (which
                        is pretty much a file), then creates a ObjectURL for that Blob. I don't know 
                        why or how, but this makes it so clicking on this downloads the dataframe.

                        For more information, see the blog post linked at the top of this file.
                    */}
                    <a 
                        href={URL.createObjectURL(new Blob(
                            [ dataframeCSV ],
                            { type: 'text/csv' }
                        ))} 
                        download={props.dfName + '.csv'}
                        className='modal-action-button modal-dual-button-right'
                        onClick={onDownload}
                    > 
                            Download 
                    </a>
                </Fragment> 
            }
        />
    )
};

export default DownloadModal;