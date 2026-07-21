import { ChevronLeft, ChevronRight, Pencil, Trash2 } from "lucide-react";
import { EmptyState } from "../ui/Feedback";

function value(row, column) {
  const raw = typeof column.value === "function" ? column.value(row) : row[column.key];
  if (column.format) return column.format(raw, row);
  if (typeof raw === "boolean") return raw ? "Yes" : "No";
  return raw ?? "—";
}

export default function DataTable({ rows, columns, onEdit, onDelete, rowActions, page, pages, setPage }) {
  if (!rows.length) return <EmptyState />;
  return <div><div className="hidden overflow-x-auto md:block"><table className="w-full text-left text-sm"><thead className="border-b bg-stone-50 text-xs uppercase tracking-wide text-stone-500"><tr>{columns.map((column) => <th key={column.key} className="whitespace-nowrap px-4 py-3">{column.label}</th>)}{(onEdit || onDelete || rowActions) && <th className="px-4 py-3 text-right">Actions</th>}</tr></thead>
    <tbody className="divide-y">{rows.map((row) => <tr key={row.id} className="hover:bg-stone-50">{columns.map((column) => <td key={column.key} className="max-w-xs px-4 py-3">{value(row, column)}</td>)}{(onEdit || onDelete || rowActions) && <td className="px-4 py-3"><div className="flex justify-end gap-1">{rowActions?.(row)}{onEdit && <button aria-label="Edit" onClick={() => onEdit(row)} className="rounded-lg p-2 hover:bg-stone-100"><Pencil className="h-4 w-4" /></button>}{onDelete && <button aria-label="Delete" onClick={() => onDelete(row)} className="rounded-lg p-2 text-red-600 hover:bg-red-50"><Trash2 className="h-4 w-4" /></button>}</div></td>}</tr>)}</tbody></table></div>
    <div className="space-y-3 md:hidden">{rows.map((row) => <article key={row.id} className="rounded-2xl border bg-white p-4">{columns.map((column, index) => <div key={column.key} className={index === 0 ? "mb-3 font-bold text-stone-900" : "flex justify-between gap-4 border-t py-2 text-sm"}><span className={index === 0 ? "hidden" : "text-stone-500"}>{column.label}</span><span className="text-right">{value(row, column)}</span></div>)}{(onEdit || onDelete || rowActions) && <div className="mt-2 flex gap-2">{rowActions?.(row)}{onEdit && <button onClick={() => onEdit(row)} className="btn-secondary flex-1"><Pencil className="h-4 w-4" />Edit</button>}{onDelete && <button onClick={() => onDelete(row)} className="btn-secondary text-red-600"><Trash2 className="h-4 w-4" /></button>}</div>}</article>)}</div>
    {pages > 1 && <div className="mt-5 flex items-center justify-between border-t pt-4 text-sm"><span>Page {page} of {pages}</span><div className="flex gap-2"><button className="btn-secondary min-h-9 px-3" disabled={page <= 1} onClick={() => setPage(page - 1)}><ChevronLeft /></button><button className="btn-secondary min-h-9 px-3" disabled={page >= pages} onClick={() => setPage(page + 1)}><ChevronRight /></button></div></div>}</div>;
}
