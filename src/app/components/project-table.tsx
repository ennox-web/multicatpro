"use client";

import {
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    getSortedRowModel,
    useReactTable
} from '@tanstack/react-table';
import { useReducer, useState } from 'react';
import { ProjectInterface, projectTestData } from '@/app/api/data/project-data';
import styles from './project-table.module.css';
import TagChipList from './tag/tag-chip-list';
import PriorityIcon from './priority-icon';


const columnHelper = createColumnHelper<ProjectInterface>();

// TODO: Drag and Drop?
// TODO: Server-side sorting - https://tanstack.com/table/v8/docs/guide/sorting
// TODO: Pagination
// TODO: Number of projects to show


const columns = [
    columnHelper.accessor('name', {
        cell: info => info.getValue(),
        header: () => <b>Name</b>,
        sortingFn: 'alphanumeric',
    }),
    columnHelper.accessor(row => row.projectType, {
        id: 'projectType',
        header: () => <b>Project Type</b>,
        sortingFn: 'alphanumeric',
    }),
    columnHelper.accessor('priority', {
        header: () => <b>Priority</b>,
        cell: info => <PriorityIcon priority={info.getValue()} />,
        sortingFn: 'alphanumeric',
    }),
    columnHelper.accessor('progress', {
        cell: info => Math.floor(info.getValue() * 100).toString() + '%',
        header: () => <b>Progress</b>,
        sortingFn: 'alphanumeric',
    }),
    columnHelper.accessor('updatedOn', {
        cell: info => info.getValue().toLocaleString(),
        header: () => <b>Last Update</b>,
        sortingFn: 'datetime',
    }),
    columnHelper.accessor('tags', {
        cell: info => {
            console.log(info.row.index, info.getValue());
            return (
                <TagChipList tags={info.getValue()} rowIndex={info.row.index} />
            )
        },
        header: () => <b>Tags</b>,
        enableSorting: false,
    })
    // columnHelper.accessor('category', {
    //     header: () => 'Category',
    //     cell: info => info.renderValue(),
    // }),
]

export default function ProjectTable() {
    const [data, _setData] = useState(() => [...projectTestData])
    const rerender = useReducer(() => ({}), {})[1]

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        initialState: {
            sorting: [
                {
                    id: 'priority',
                    desc: true,
                },
            ],
        },
    });

    return (
        <div>
            {/* Render the table */}
            <div className={styles.tableWrapper}>
                <table className={styles.table}>
                    <thead>
                        {/* Render table headers */}
                        {table.getHeaderGroups().map((headerGroup) => (
                            <tr key={headerGroup.id} className={styles.tableHeaderRow}>
                                {headerGroup.headers.map((header, index) => (
                                    <th colSpan={header.colSpan} key={header.id} className={styles.tableHeader}>
                                        {/* Render header content or leave blank if it's a placeholder */}
                                        {header.isPlaceholder ? null : (
                                            <div className={
                                                header.column.getCanSort() ? `${styles.headerSorter}` : ''
                                            }
                                                onClick={header.column.getToggleSortingHandler()}
                                                title={
                                                    header.column.getCanSort() ? header.column.getNextSortingOrder() === 'asc' ? 'Sort ascending' :
                                                        header.column.getNextSortingOrder() === 'desc' ? 'Sort descending' : 'Clear sort'
                                                        : undefined
                                                }
                                            >
                                                {
                                                    flexRender(
                                                        header.column.columnDef.header, // Header definition
                                                        header.getContext(), // Context for the header
                                                    )
                                                }
                                                {{
                                                    asc: <span className='material-symbols-outlined'>arrow_drop_up</span>,
                                                    desc: <span className='material-symbols-outlined'>arrow_drop_down</span>
                                                }[header.column.getIsSorted() as string] ?? null}
                                            </div>
                                        )}
                                    </th>
                                ))}
                            </tr>
                        ))}
                    </thead>
                    <tbody>
                        {/* Render table rows */}
                        {table.getRowModel().rows.map((row) => (
                            <tr key={row.id} className={styles.tableRow}>
                                {row.getVisibleCells().map((cell) => (
                                    <td key={cell.id} className={styles.tableCell}>
                                        {/* Render each cell's content */}
                                        {flexRender(
                                            cell.column.columnDef.cell, // Cell definition
                                            cell.getContext() // Context for the cell
                                        )}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

/*
            <button onClick={() => rerender()} className="border p-2">
                Rerender
            </button>
            */