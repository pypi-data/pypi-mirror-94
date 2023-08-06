// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect } from 'react';

// import css
import "../../../../css/margins.css";
import { MitoAPI } from '../../../api';


type ColumnSummaryGraphProps = {
    selectedSheetIndex: number;
    columnHeader: string;
    mitoAPI: MitoAPI;
}

/*
    Displays the column summary graph in the column control panel
*/
function ColumnSummaryGraph(props: ColumnSummaryGraphProps): JSX.Element {
    const [base64PNGImage, setBase64PNGImage] = useState('');
    const [alt, setAlt] = useState('Graph is loading...');

    async function loadBase64PNGImage() {
        const loadedBase64PNGImage = await props.mitoAPI.getColumnSummaryGraph(props.selectedSheetIndex, props.columnHeader);
        if (loadedBase64PNGImage === '') {
            setAlt('Sorry, it looks like there are too many items in this column to display them well.')
        } else {
            setBase64PNGImage(loadedBase64PNGImage);
        }
    }

    useEffect(() => {
        void loadBase64PNGImage();
    }, [])

    return (
        <React.Fragment>
            <div className='filter-modal-section-title'>
                <p> Column Summary Graph </p>
            </div>
            <img className='mb-2' src={'data:image/png;base64, ' + base64PNGImage} alt={alt}/>
        </React.Fragment>
    );
}


export default ColumnSummaryGraph;