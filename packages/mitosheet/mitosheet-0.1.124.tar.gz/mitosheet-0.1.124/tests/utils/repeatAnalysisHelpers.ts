// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for repeating an analysis.
*/

import { Selector } from 'testcafe';
import { modalAdvanceButtonSelector } from './allModals';
import { DELETE_PRESS_KEYS_STRING } from './helpers';
import { dfNamesStringSelector, rawPythonCodeblockSelector, simpleImportSelect, simpleImportSelectOption } from './importHelpers'


export const repeatAnalysisButton = Selector('div')
    .withExactText('Repeat Saved Analysis')
    .parent()

/* 
    Helper function that returns a selector for a saved analysis in the
    saved analysis list
*/
export const getSavedAnalysisItem = (savedAnalysisName: string): Selector => {    
    return Selector('input')
        .withAttribute('name', savedAnalysisName)
}


/*
    Repeats the analysis with the given name
*/
export async function repeatAnalysis(t: TestController, analysisName: string): Promise<void> {
    await t
        .click(repeatAnalysisButton)
        .click(getSavedAnalysisItem(analysisName))
        .click(modalAdvanceButtonSelector)
}


/*
    If repeating an analysis with imports, this changes the files
    that are imported, as well as the pythonCode 
*/
export async function repeatAnalysisChangeImports(t: TestController, newImports: {file_names?: string[]; rawPythonImports?: {pythonCode: string; dfNamesString: string}[]}): Promise<void> {
    // Wait a bit, for data to load
    await t.wait(500);

    for (let i = 0; i < newImports.file_names?.length; i++) {
        const fileName = newImports.file_names[i];
        await t
            .click(simpleImportSelect.nth(i))
            .click(simpleImportSelectOption.withExactText(fileName).nth(i))
    }

    for (let i = 0; i < newImports.rawPythonImports?.length; i++) {
        const pythonCode = newImports.rawPythonImports[i].pythonCode;
        const dfNamesString = newImports.rawPythonImports[i].dfNamesString;

        await t
            // Delete things
            .click(rawPythonCodeblockSelector.nth(i))
            .pressKey(DELETE_PRESS_KEYS_STRING)
            .click(dfNamesStringSelector.nth(i))
            .pressKey(DELETE_PRESS_KEYS_STRING)
            .typeText(rawPythonCodeblockSelector.nth(i), pythonCode)
            .typeText(dfNamesStringSelector.nth(i), dfNamesString)
    }

    await t.click(modalAdvanceButtonSelector)
}
