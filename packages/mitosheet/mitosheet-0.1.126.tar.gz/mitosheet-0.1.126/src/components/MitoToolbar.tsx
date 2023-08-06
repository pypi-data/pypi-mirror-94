// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from 'react';
import fscreen from 'fscreen';

// Import CSS
import "../../css/mito-toolbar.css"
import "../../css/margins.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';
import { TaskpaneInfo, TaskpaneType } from './taskpanes/taskpanes';
import { MitoAPI } from '../api';

const MitoToolbar = (
    props: {
        mitoContainerRef: HTMLDivElement | undefined | null,
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        setEditingMode: (on: boolean, column: string, rowIndex: number) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string,
        selectedColumn: string,
        setCurrOpenTaskpane: (newCurrTaskpane: TaskpaneInfo) => void;
        mitoAPI: MitoAPI
        closeOpenEditingPopups: () => void;
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        /*
        * Helper function that, given a number, returns Excel column that corresponds to this number (1-indexed)
        */
        function toColumnName(num: number): string {
            let ret;
            let a = 1;
            let b = 26;
            for (ret = ''; (num -= a) >= 0; a = b, b *= 26) {
                ret = String.fromCharCode(Math.round((num % b) / a) + 65) + ret;
            }
            return ret;
        }

        let inc = 1;
        let newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        // If the column header is in the sheet already, we bump and keep trying
        while (props.sheetJSON.columns.includes(newColumnHeader)) {
            inc++;
            newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        }
        void props.mitoAPI.sendColumnAddMessage(
            props.selectedSheetIndex,
            newColumnHeader
        );
    }


    /* Undoes the last step that was created */
    const undo = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        void props.mitoAPI.sendUndoMessage();
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setModal({type: ModalEnum.Download});
    }

    
    const [fullscreen, setFullscreen] = useState(false);
    fscreen.onfullscreenchange = () => {
        setFullscreen(!!fscreen.fullscreenElement)


        
        void props.mitoAPI.sendLogMessage(
            'button_toggle_fullscreen',
            {
                // Note that this is true when _end_ in fullscreen mode, and 
                // false when we _end_ not in fullscreen mode, which is much
                // more natural than the alternative
                fullscreen: !!fscreen.fullscreenElement
            }
        )
    };
    /* 
        Toggles if Mito is full screen or not
    */
    const toggleFullscreen = () => {
        // We toggle to the opposite of whatever the fullscreen actually is (as detected by the
        // fscreen library), and then we set the fullscreen state variable to that state (in the callback
        // above), so that the component rerenders propery
        const isNotFullscreen = fscreen.fullscreenElement === undefined || fscreen.fullscreenElement === null;
        if (isNotFullscreen && props.mitoContainerRef) {
            fscreen.requestFullscreen(props.mitoContainerRef);
        } else {
            fscreen.exitFullscreen();
        }
    }

    const openDocumentation = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We log the opening of the documentation taskpane
        void props.mitoAPI.sendLogMessage(
            'button_documentation_log_event',
            {
                stage: 'opened'
            }
        );

        // we open the documentation taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.DOCUMENTATION});
    }

    const openMerge = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We open the merge taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.MERGE});
    }

    const openPivotTable = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setCurrOpenTaskpane({type: TaskpaneType.PIVOT});
    }

    const openDeleteColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        // TODO: log here, and in all the rest of these functions

        props.setModal({type: ModalEnum.DeleteColumn, columnHeader: props.selectedColumn});
    }

    const openSave = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setModal({type: ModalEnum.SaveAnalysis});
    }

    
    const openReplay = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setModal({type: ModalEnum.ReplayAnalysis});
    }
    
    const openImport = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setModal({type: ModalEnum.Import});
    }

    const contactSupport = () => {
        // log that they clicked the contact support button
        void props.mitoAPI.sendLogMessage('button_talk_to_support')

        // open Hubspot
        window.open("https://hubs.ly/H0FL1920", '_blank')
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-container-left'>
                <button className='mito-toolbar-item vertical-align-content' onClick={undo}>
                    <svg width="24" height="10" viewBox="0 0 12 5" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0.802595 2.66537C0.719857 2.77576 0.741164 2.93409 0.850186 3.01899C0.959208 3.10389 1.11466 3.08322 1.1974 2.97283L0.802595 2.66537ZM2.54776 0.753934L2.67568 0.538802C2.56722 0.47157 2.42691 0.498052 2.35035 0.600204L2.54776 0.753934ZM4.73383 2.4034C4.85105 2.47605 5.00334 2.43863 5.074 2.31982C5.14465 2.20101 5.1069 2.04579 4.98968 1.97313L4.73383 2.4034ZM1.1974 2.97283L2.74516 0.907664L2.35035 0.600204L0.802595 2.66537L1.1974 2.97283ZM2.41983 0.969067L4.73383 2.4034L4.98968 1.97313L2.67568 0.538802L2.41983 0.969067Z" fill="#343434"/>
                        <path d="M11.5 0C11.5 2.41714 9.03395 4.37659 6.60866 4.37659C4.64237 4.37659 3.05958 2.77564 2.5 1" stroke="#343434" strokeWidth="0.6"/>
                    </svg>
                    {/* Extra styling to make sure the tooltip doesn't float off the screen*/}
                    <Tooltip tooltip={"Undo"} style={{'marginLeft': '-15px'}}/>
                </button>

                <div className="vertical-line mt-1"/>

                <button className='mito-toolbar-item vertical-align-content' id='tour-import-button-id' onClick={openImport}>
                    <svg width="25" height="25" viewBox="0 0 7 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3.48679 1.24113L3.48679 8.00001" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                        <path d="M0.165052 4.05751C0.069509 4.15719 0.0728591 4.31544 0.172534 4.41099C0.27221 4.50653 0.430465 4.50318 0.526009 4.4035L0.165052 4.05751ZM3.44212 0.999984L3.62013 0.824442C3.57271 0.776365 3.50787 0.749511 3.44035 0.749991C3.37283 0.75047 3.30837 0.778243 3.26164 0.826988L3.44212 0.999984ZM6.45001 4.40605C6.54696 4.50436 6.70525 4.50546 6.80356 4.40851C6.90186 4.31156 6.90296 4.15327 6.80601 4.05497L6.45001 4.40605ZM0.526009 4.4035L3.6226 1.17298L3.26164 0.826988L0.165052 4.05751L0.526009 4.4035ZM3.26412 1.17553L6.45001 4.40605L6.80601 4.05497L3.62013 0.824442L3.26412 1.17553Z" fill="#343434"/>
                    </svg>

                    <Tooltip tooltip={"Import Data"}/>
                </button>

                <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                    <svg width="25" height="25" viewBox="0 0 7 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3.51321 7.75887L3.51321 0.999992" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                        <path d="M6.83495 4.94249C6.93049 4.84281 6.92714 4.68456 6.82747 4.58901C6.72779 4.49347 6.56953 4.49682 6.47399 4.5965L6.83495 4.94249ZM3.55788 8.00002L3.37987 8.17556C3.42729 8.22364 3.49213 8.25049 3.55965 8.25001C3.62717 8.24953 3.69163 8.22176 3.73836 8.17301L3.55788 8.00002ZM0.54999 4.59395C0.45304 4.49564 0.294753 4.49454 0.196445 4.59149C0.0981369 4.68844 0.0970358 4.84673 0.193985 4.94503L0.54999 4.59395ZM6.47399 4.5965L3.3774 7.82702L3.73836 8.17301L6.83495 4.94249L6.47399 4.5965ZM3.73588 7.82447L0.54999 4.59395L0.193985 4.94503L3.37987 8.17556L3.73588 7.82447Z" fill="#343434"/>
                    </svg>
                    <Tooltip tooltip={"Download Sheet"}/>
                </button>

                <div className="vertical-line mt-1"/>

                <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                    <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6.45456 1V2.81818" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                        <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.6" strokeLinecap="round"/>
                        <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                    </svg>
                    <Tooltip tooltip={"Add Column"}/>
                </button>
                <button className='mito-toolbar-item vertical-align-content' onClick={openDeleteColumn}>
                    <svg width="20" height="28" viewBox="0 0 7 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5.99142 10.75H1.0641C0.956936 10.75 0.867939 10.6673 0.860102 10.5604L0.285102 2.7195C0.276409 2.60096 0.370239 2.5 0.489099 2.5H6.51414C6.63246 2.5 6.72611 2.60009 6.71823 2.71815L6.19551 10.5591C6.18834 10.6665 6.0991 10.75 5.99142 10.75Z" stroke="#343434" strokeWidth="0.6"/>
                        <path d="M1.60416 2.41164V1.375V0.733332H5.45416V2.41165" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M2.56668 4.58334L2.5666 8.43335" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M4.49167 4.58334L4.49158 8.43335" stroke="#343434" strokeWidth="0.6" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <Tooltip tooltip={"Delete Column"}/>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className='mito-toolbar-item' onClick={openPivotTable}>
                    <svg width="30" height="30" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="1.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="1.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="8.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="8.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
                        <circle cx="3" cy="3" r="1" fill="#343434"/>
                        <circle cx="5" cy="5" r="1" fill="#343434"/>
                        <path d="M9.49994 2.49992L9.49992 5.5M12.5 2.5L12.4999 5.50008M10.9999 2.50014L10.9999 5.50022" stroke="#343434" strokeWidth="0.6"/>
                        <path d="M5.63898 9.5L2.32331 9.5M5.63901 12.3181L3.97868 12.3182L2.31834 12.3183M5.63898 10.8809L2.31834 10.8809" stroke="#343434" strokeWidth="0.6"/>
                    </svg>
                    <Tooltip tooltip={"Pivot Table"}/>
                </button>
                <button className='mito-toolbar-item' onClick={openMerge}>
                    <svg width="40" height="30" viewBox="0 0 17 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11.6467 5.12789C11.6467 7.78833 9.13157 10.0058 5.94835 10.0058C2.76513 10.0058 0.25 7.78833 0.25 5.12789C0.25 2.46744 2.76513 0.25 5.94835 0.25C9.13157 0.25 11.6467 2.46744 11.6467 5.12789Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.6"/>
                        <path d="M16.4784 5.12789C16.4784 7.78833 13.9632 10.0058 10.78 10.0058C7.59679 10.0058 5.08167 7.78833 5.08167 5.12789C5.08167 2.46744 7.59679 0.25 10.78 0.25C13.9632 0.25 16.4784 2.46744 16.4784 5.12789Z" stroke="#343434" strokeWidth="0.6"/>
                    </svg>
                    <Tooltip tooltip={"Merge"}/>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className='mito-toolbar-item' onClick={openSave}>
                    <svg width="25" height="25" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 10.75H2C1.0335 10.75 0.25 9.9665 0.25 9V2C0.25 1.0335 1.0335 0.25 2 0.25H5.40054C5.81012 0.25 6.20673 0.393662 6.52129 0.655968L9.12075 2.82358C9.51948 3.15607 9.75 3.64844 9.75 4.16761V9C9.75 9.9665 8.9665 10.75 8 10.75Z" stroke="#343434" strokeWidth="0.6"/>
                        <rect x="2.12503" y="6.05005" width="5.875" height="0.75" fill="#343434"/>
                        <rect x="4.375" y="2.88745" width="2.8875" height="0.75" transform="rotate(-90 4.375 2.88745)" fill="#343434"/>
                        <rect x="2.12503" y="8.11255" width="5.875" height="0.75" fill="#343434"/>
                    </svg>
                    <Tooltip tooltip={"Save"}/>
                </button>
                <button className='mito-toolbar-item' onClick={openReplay}>
                    <svg width="30" height="30" viewBox="0 0 14 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0.799219 8.65346C0.713311 8.76181 0.733559 8.91606 0.844444 8.99798C0.955329 9.07989 1.11486 9.05846 1.20077 8.95011L0.799219 8.65346ZM2.65464 6.71478L2.788 6.50394C2.6775 6.4392 2.53338 6.46616 2.45387 6.56645L2.65464 6.71478ZM4.9951 8.37511C5.11448 8.44506 5.27096 8.40737 5.34461 8.29093C5.41825 8.17449 5.38118 8.02339 5.2618 7.95344L4.9951 8.37511ZM1.20077 8.95011L2.85542 6.8631L2.45387 6.56645L0.799219 8.65346L1.20077 8.95011ZM2.52129 6.92561L4.9951 8.37511L5.2618 7.95344L2.788 6.50394L2.52129 6.92561Z" fill="#343434"/>
                        <path d="M11.6906 5.95284C11.6906 8.39554 9.58876 10.3757 6.99598 10.3757C4.89389 10.3757 3.09822 8.79442 2.5 7" stroke="#343434" strokeWidth="0.6"/>
                        <path d="M13.2008 2.80751C13.2867 2.69916 13.2664 2.54491 13.1556 2.46299C13.0447 2.38107 12.8851 2.40251 12.7992 2.51086L13.2008 2.80751ZM11.3454 4.74619L11.212 4.95702C11.3225 5.02177 11.4666 4.99481 11.5461 4.89451L11.3454 4.74619ZM9.0049 3.08586C8.88552 3.01591 8.72904 3.0536 8.65539 3.17004C8.58175 3.28648 8.61882 3.43758 8.7382 3.50753L9.0049 3.08586ZM12.7992 2.51086L11.1446 4.59786L11.5461 4.89451L13.2008 2.80751L12.7992 2.51086ZM11.4787 4.53535L9.0049 3.08586L8.7382 3.50753L11.212 4.95702L11.4787 4.53535Z" fill="#343434"/>
                        <path d="M2.30938 5.5081C2.30938 3.0654 4.41124 1.08521 7.00402 1.08521C9.10611 1.08521 10.9018 2.70558 11.5 4.5" stroke="#343434" strokeWidth="0.6"/>
                    </svg>
                    <Tooltip tooltip={"Repeat Saved Analysis"}/>
                </button>
            </div>
            <div className='mito-toolbar-container-right mr-1'>
                <button className='mito-toolbar-item mito-toolbar-talk-to-support-button' onClick={contactSupport}>
                    Talk to Support
                </button>
                <button className='mito-toolbar-item' onClick={openDocumentation}>
                    <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="7" cy="7" r="6.75" stroke="#404040" strokeWidth="0.6"/>
                        <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                    </svg>
                    <Tooltip tooltip={"Documentation"} />
                </button>
                <button className='mito-toolbar-item' onClick={toggleFullscreen}>
                    {/* We show a different icon depending if it is fullscreen or not*/}
                    {fullscreen &&
                        <svg width="25" height="25" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9.69561 5.99947C9.69531 6.16516 9.82939 6.29971 9.99508 6.3L12.6951 6.30476C12.8608 6.30505 12.9953 6.17097 12.9956 6.00529C12.9959 5.8396 12.8618 5.70505 12.6961 5.70476L10.2961 5.70053L10.3004 3.30053C10.3007 3.13485 10.1666 3.0003 10.0009 3C9.83521 2.99971 9.70066 3.13379 9.70037 3.29948L9.69561 5.99947ZM13.798 1.78749L9.78385 5.78749L10.2074 6.21251L14.2215 2.21251L13.798 1.78749Z" fill="#343434"/>
                            <path d="M6.29488 9.97918C6.28338 9.81389 6.14007 9.68923 5.97479 9.70072L3.2813 9.88809C3.11601 9.89959 2.99134 10.0429 3.00284 10.2082C3.01434 10.3735 3.15765 10.4981 3.32293 10.4866L5.71715 10.3201L5.8837 12.7143C5.8952 12.8796 6.03851 13.0043 6.2038 12.9928C6.36908 12.9813 6.49375 12.838 6.48225 12.6727L6.29488 9.97918ZM2.50897 14.4651L6.22195 10.1969L5.76926 9.8031L2.05628 14.0713L2.50897 14.4651Z" fill="#343434"/>
                            <path d="M9.9883 9.70009C9.82266 9.70412 9.69166 9.84167 9.69569 10.0073L9.76146 12.7065C9.76549 12.8721 9.90304 13.0031 10.0687 12.9991C10.2343 12.9951 10.3653 12.8575 10.3613 12.6919L10.3028 10.2926L12.7021 10.2341C12.8677 10.2301 12.9988 10.0926 12.9947 9.92693C12.9907 9.76129 12.8531 9.63029 12.6875 9.63433L9.9883 9.70009ZM14.3578 13.7403L10.2025 9.78276L9.7887 10.2172L13.9439 14.1748L14.3578 13.7403Z" fill="#343434"/>
                            <path d="M5.99905 6.29998C6.16473 6.29808 6.29749 6.16223 6.29559 5.99655L6.26456 3.29673C6.26266 3.13106 6.12681 2.99829 5.96113 3.0002C5.79546 3.0021 5.6627 3.13795 5.6646 3.30363L5.69218 5.70347L3.29234 5.73105C3.12666 5.73295 2.9939 5.8688 2.9958 6.03447C2.99771 6.20015 3.13356 6.33291 3.29923 6.33101L5.99905 6.29998ZM1.79032 2.30974L5.78592 6.21456L6.20529 5.78544L2.20968 1.88063L1.79032 2.30974Z" fill="#343434"/>
                        </svg>
                    }
                    {!fullscreen &&
                        <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M13.3141 1.00002C13.3141 0.834334 13.1798 0.700019 13.0141 0.70002L10.3141 0.700019C10.1484 0.70002 10.0141 0.834334 10.0141 1.00002C10.0141 1.1657 10.1484 1.30002 10.3141 1.30002H12.7141V3.70002C12.7141 3.8657 12.8484 4.00002 13.0141 4.00002C13.1798 4.00002 13.3141 3.86571 13.3141 3.70002L13.3141 1.00002ZM8.07966 6.35874L13.2262 1.21215L12.802 0.787887L7.65539 5.93447L8.07966 6.35874Z" fill="#343434"/>
                            <path d="M0.799699 13.105C0.80268 13.2707 0.939389 13.4026 1.10505 13.3996L3.80461 13.351C3.97027 13.348 4.10215 13.2113 4.09916 13.0457C4.09618 12.88 3.95947 12.7481 3.79382 12.7511L1.3942 12.7943L1.35103 10.3947C1.34805 10.229 1.21134 10.0971 1.04568 10.1001C0.880021 10.1031 0.748145 10.2398 0.751125 10.4055L0.799699 13.105ZM5.93609 7.65384L0.883736 12.8913L1.31556 13.3079L6.36792 8.0704L5.93609 7.65384Z" fill="#343434"/>
                            <path d="M13.1141 13.2999C13.2798 13.2997 13.4139 13.1652 13.4137 12.9995L13.4105 10.2995C13.4103 10.1338 13.2759 9.99968 13.1102 9.99987C12.9445 10.0001 12.8103 10.1345 12.8105 10.3002L12.8134 12.7002L10.4134 12.7031C10.2477 12.7033 10.1135 12.8377 10.1137 13.0034C10.1139 13.1691 10.2484 13.3033 10.4141 13.3031L13.1141 13.2999ZM7.74918 8.07176L12.9019 13.2123L13.3256 12.7875L8.17294 7.64699L7.74918 8.07176Z" fill="#343434"/>
                            <path d="M0.994269 0.799772C0.828614 0.802948 0.696899 0.939813 0.700076 1.10547L0.751844 3.80497C0.755021 3.97063 0.891886 4.10234 1.05754 4.09916C1.2232 4.09599 1.35491 3.95912 1.35173 3.79347L1.30572 1.39391L3.70528 1.34789C3.87093 1.34472 4.00265 1.20785 3.99947 1.0422C3.99629 0.876542 3.85943 0.744827 3.69377 0.748004L0.994269 0.799772ZM6.45153 5.92971L1.20805 0.883556L0.791995 1.31588L6.03547 6.36203L6.45153 5.92971Z" fill="#343434"/>
                        </svg>
                    }
                    
                    {/* Extra styling to make sure the full screen tooltip doesn't float off the screen*/}
                    <Tooltip tooltip={fullscreen ? "Close Full Screen": "Full Screen"} style={{'marginLeft': '-80.5px'}}/>
                </button>
            </div>
        </div>
    );
};

export default MitoToolbar;