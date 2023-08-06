// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ColumnType } from '../../Mito';

// import css
import "../../../../css/margins.css";
import "../../../../css/filter_modal.css"
import { MitoAPI } from '../../../api';


/*
Implementation plan:
- There is a set of displayed filters, but they are not the set of applied filters.
- The displayed filters D, are a superset of the applied filters F.
- The applied fitlers, F, are D - the filters that have _no_ text in them. We only apply a filters
  with something in them
*/

export enum SharedFilterCondition {
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty'
}

export enum StringFilterCondition {
    CONTAINS = 'contains',
    DOES_NOT_CONTAIN = 'string_does_not_contain',
    STRING_EXACTLY = 'string_exactly'
}

export enum NumberFilterCondition {
    NUMBER_EXACTLY = 'number_exactly',
    GREATER = 'greater',
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal',
    LESS = 'less',
    LESS_THAN_OR_EQUAL = 'less_than_or_equal',
}

export enum DateFilterCondition {
    DATETIME_EXTACTLY = 'datetime_exactly',
    DATETIME_GREATER_THAN = 'datetime_greater',
    DATETIME_GREATER_THAN_OR_EQUAL = 'datetime_greater_than_or_equal',
    DATETIME_LESS = 'datetime_less',
    DATETIME_LESS_THAN_OR_EQUAL = 'datetime_less_than_or_equal',
}

export type FilterCondition = 
    | SharedFilterCondition
    | StringFilterCondition
    | NumberFilterCondition
    | DateFilterCondition

interface StringFilterType {
    type: 'string',
    condition: FilterCondition,
    value?: string
}

interface NumberFilterType {
    type: 'number',
    condition: FilterCondition,
    value?: number | string
}

interface DateFilterType {
    type: 'datetime',
    condition: FilterCondition,
    value?: string
}

export type FilterObjectArray  = {
    type: "string" | "number" | "datetime";
    condition: FilterCondition;
    value: string | number;
}[]


export type FiltersTypes = (StringFilterType | NumberFilterType | DateFilterType)[];

type FilterModalProps = {
    selectedSheetIndex: number,
    columnHeader: string,
    filters: FiltersTypes,
    columnType: ColumnType;
    operator: 'And' | 'Or',
    mitoAPI: MitoAPI,
}

interface FilterModalState {
    /* 
        Displayed filters are the filters that are the shown to the user, which must be a superset
        of the filters that are actually applied to the column.
 
        However, not all displayed filters are applied. This is because these filters may be invalid,
        for example, if they have an empty value field, or the string they input cannot be cast
        to a number (which it should be able to be).
    */
    displayedFilters: FiltersTypes,
    operator: 'And' | 'Or',
    stepID: string;
}


// if one of these filters are selected, don't display the value input
const noInputFilters: FilterCondition[] = [SharedFilterCondition.EMPTY, SharedFilterCondition.NOT_EMPTY]

const getNumberDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={NumberFilterCondition.NUMBER_EXACTLY}>=</option>
            <option value={NumberFilterCondition.GREATER}>&gt;</option>
            <option value={NumberFilterCondition.GREATER_THAN_OR_EQUAL}>&ge;</option>
            <option value={NumberFilterCondition.LESS}>&lt;</option>
            <option value={NumberFilterCondition.LESS_THAN_OR_EQUAL}>&le;</option>
        </React.Fragment>
    )
}

const getStringDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={StringFilterCondition.CONTAINS}>contains</option>
            <option value={StringFilterCondition.DOES_NOT_CONTAIN}>does not contain</option>
            <option value={StringFilterCondition.STRING_EXACTLY}>is exactly</option>
        </React.Fragment>
    )
}

const getDatetimeDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={DateFilterCondition.DATETIME_EXTACTLY}>=</option>
            <option value={DateFilterCondition.DATETIME_GREATER_THAN}>&gt;</option>
            <option value={DateFilterCondition.DATETIME_GREATER_THAN_OR_EQUAL}>&ge;</option>
            <option value={DateFilterCondition.DATETIME_LESS}>&lt;</option>
            <option value={DateFilterCondition.DATETIME_LESS_THAN_OR_EQUAL}>&le;</option>
        </React.Fragment>
    )
}

const getSharedDropdownOptions = () => {
    return (
        <React.Fragment>
            <option value={SharedFilterCondition.EMPTY}>is empty</option>
            <option value={SharedFilterCondition.NOT_EMPTY}>is not empty</option>
        </React.Fragment>
    )
}

const getNewEmptyFilter = (columnType: ColumnType): StringFilterType | NumberFilterType | DateFilterType => {
    switch (columnType) {
        case 'string':
            return {
                type: 'string',
                condition: StringFilterCondition.CONTAINS,
                value: ''
            }
        case 'number':
            return {
                type: 'number',
                condition: NumberFilterCondition.NUMBER_EXACTLY,
                value: ''
            }
        case 'datetime':
            return {
                type: 'datetime',
                condition: DateFilterCondition.DATETIME_EXTACTLY,
                value: ''
            }
    }
}


/*
    A modal that allows a user to filter a column
*/
class FilterCard extends React.Component<FilterModalProps, FilterModalState> {

    constructor(props: FilterModalProps) {
        super(props);

        this.state = {
            displayedFilters: this.props.filters,
            operator: this.props.operator,
            stepID: ''
        }

        this.buildFilters = this.buildFilters.bind(this);
        this.sendFilterUpdateMessage = this.sendFilterUpdateMessage.bind(this);
    }

    async sendFilterUpdateMessage(): Promise<void> {

        // Before sending the displayed filters, we:
        // 1. Change all undefined values (like this in conditions without values) to 0's,
        // 2. Filter out all the filters that have an empty string as the value
        const filtersToApply = this.state.displayedFilters.map(filter => {
            return {
                'type': filter.type,
                'condition': filter.condition,
                'value': filter.value === undefined ? 0 : filter.value
            }
        }).filter(filter => {
            return filter['value'] !== '';
        });

        const stepID = await this.props.mitoAPI.sendFilterMessage(
            this.props.selectedSheetIndex,
            this.props.columnHeader,
            filtersToApply,
            this.state.operator,
            this.state.stepID
        )

        this.setState({stepID: stepID})
    }

    /*
        Builds all the JSX for the filter selections, for all of the filters in
        this.state.filters
    */
    buildFilters(): JSX.Element {

        /*
            Occurs when the user changes what operator is operating
            on the filter conditions.
        */
        const handleToggleOperator = (e: React.ChangeEvent<HTMLSelectElement>): void => {
            const newOperator = e.target.value as 'And' | 'Or';
            this.setState({
                operator: newOperator
            }, () => {
                void this.sendFilterUpdateMessage();
            })
        }

        /*
            A helper function to update the filter condition for a specific index
        */
        const handleConditionChange = (filterIndex: number, e: React.ChangeEvent<HTMLSelectElement>): void => {            
            // This case is safe, as users can only select from a list of the enum
            const newCondition = e.target.value as FilterCondition;

            this.setState(prevState => {
                const newFilters = [...prevState.displayedFilters];
                newFilters[filterIndex].condition = newCondition
                if (noInputFilters.includes(newCondition)) {
                    // Clear the value, if this condition has no value
                    newFilters[filterIndex].value = undefined;
                } else {
                    // Otherwise, set it to the empty string, if it does not have a value current
                    if (newFilters[filterIndex].value === undefined) {
                        newFilters[filterIndex].value = '';
                    }
                }
                return {displayedFilters: newFilters}
            }, () => {
                // once state is updated, send the filter message
                void this.sendFilterUpdateMessage()
            })
        }

        /* 
            Occurs when the user  changes the 
        */
        const handleValueChange = (filterIndex: number, e: React.ChangeEvent<HTMLInputElement>): void => {
            // Occurs when the user changes a value on a specific filter, which is then
            // saved to the state for this filter

            const filter = this.state.displayedFilters[filterIndex];
            let newValue: string | number = e.target.value;
            // Cast it to the correct type, aka turn it to a number if this is a number filter
            if (filter.type === 'number') {
                const float = parseFloat(newValue);
                if (!Number.isNaN(float)) {
                    newValue = float;
                }
            }

            this.setState(prevState => {
                const newFilters = [...prevState.displayedFilters] as FiltersTypes;
                // Note: we save the new condition outside the setState, as react does
                // not keep events around! 
                newFilters[filterIndex].value = newValue;

                return {
                    displayedFilters: newFilters,
                }
            }, () => {
                // once state is updated, try sending the filter message
                void this.sendFilterUpdateMessage()
            })
        }

        const removeFilter = (filterIndex: number): void => {
            // Removes the filter at the given filterIndex 

            this.setState(prevState => {
                const newFilters = [...prevState.displayedFilters];
                newFilters.splice(filterIndex, 1);
                return {
                    displayedFilters: newFilters
                }
            }, () => {
                // once state is updated, try sending the filter message
                void this.sendFilterUpdateMessage()
            })
        }

        const getFilter = (filter: NumberFilterType | StringFilterType | DateFilterType, filterIndex: number): JSX.Element => {
            // Builds the table row element for a given filter at a given index

            // We use styles to hide divs we don't want, to keep the spacing the same
            const operatorStyle: {visibility: 'hidden' | 'visible'} = filterIndex === 0 ? {visibility: 'hidden'} : {visibility: 'visible'};
            const inputStyle: {visibility: 'hidden' | 'visible'} = noInputFilters.includes(filter.condition) ? {visibility: 'hidden'} : {visibility: 'visible'};

            return (
                <React.Fragment key={filterIndex}>
                    <tr>
                        <td>
                            <select className='select filter-modal-input' style={operatorStyle} value={this.state.operator} onChange={handleToggleOperator} >
                                <option value={'And'}>And</option>
                                <option value={'Or'}>Or</option>
                            </select>
                        </td>
                        <td>
                            <select className="select filter-modal-condition-select" value={filter.condition} onChange={e => handleConditionChange(filterIndex, e)} >
                                {filter.type === 'number' && getNumberDropdownOptions()}
                                {filter.type === 'string' && getStringDropdownOptions()}
                                {filter.type === 'datetime' && getDatetimeDropdownOptions()}
                                {getSharedDropdownOptions()}
                            </select>
                        </td>
                        <td>
                            <input type={filter.type === 'datetime' ? 'date' : 'text'} className="input filter-modal-value-input" style={inputStyle} value={filter.value?.toString()} onChange={e => handleValueChange(filterIndex, e)}/>
                        </td>
                        <td>
                            <div className='ml-1 mr-1' onClick={() => removeFilter(filterIndex)}>
                                <svg width="13" height="3" viewBox="0 0 13 3" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="13" height="3" rx="1" fill="#B1B1B1"/>
                                </svg>
                            </div>    
                        </td>
                    </tr>
                </React.Fragment>
            )
        }

        return (
            <table>
                <tbody>
                    {this.state.displayedFilters.length > 0 &&
                            <tr>
                                <td/>
                                <td>Filter Condition</td>
                                <td>Value</td>
                            </tr>
                    }   
                    {this.state.displayedFilters.map((filter, filterIndex) => {
                        return getFilter(filter, filterIndex);
                    })}
                </tbody>
            </table>
        )
    }

    render(): JSX.Element {

        const addFilter = () => {
            this.setState(prevState => {
                const newFilters = [...prevState.displayedFilters]
                newFilters.push(getNewEmptyFilter(this.props.columnType));
                return {
                    displayedFilters: newFilters
                }
            }, () => {
                void this.sendFilterUpdateMessage()
            })
        }

        return (
            <div>
                <div className='filter-modal-section-title filter-modal-section-spacer'>
                    <p> Filter </p>
                </div>
                <div className="filter-modal-centering-container">
                    {this.state.displayedFilters.length === 0 &&
                        <p className='mb-1'>
                            Hit the Add Filter button below to begin filtering
                            this column.
                        </p>
                    }
                    {this.buildFilters()}
                    <div className='filter-modal-add-value' onClick={addFilter}>
                        + Add Filter
                    </div>
                </div>
            </div>
        );
    }
}

export default FilterCard;