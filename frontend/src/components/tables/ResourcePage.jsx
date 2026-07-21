import { useCallback, useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";
import { useSearchParams } from "react-router-dom";
import { toast } from "sonner";
import { useAuth } from "../../features/auth/AuthContext";
import { api, apiError, results } from "../../lib/api";
import DynamicForm from "../forms/DynamicForm";
import { ErrorState, LoadingScreen } from "../ui/Feedback";
import Modal from "../ui/Modal";
import PageHeader from "../ui/PageHeader";
import DataTable from "./DataTable";

export default function ResourcePage({ title, description, endpoint, columns, fields = [], readOnly = false, workerCreate = false, createOnly = false, allowDelete = true, embedded = false, rowActions }) {
  const { canManage } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const editable = !readOnly && (canManage || workerCreate);
  const [rows, setRows] = useState([]); const [count, setCount] = useState(0);
  const [page, setPage] = useState(1); const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const [editing, setEditing] = useState(null); const [modal, setModal] = useState(false);
  const load = useCallback(async () => {
    setLoading(true); setError("");
    try { const { data } = await api.get(endpoint, { params: { page, search: search || undefined } }); setRows(results(data)); setCount(data.count ?? results(data).length); }
    catch (err) { setError(apiError(err)); } finally { setLoading(false); }
  }, [endpoint, page, search]);
  useEffect(() => { const timer = setTimeout(load, 250); return () => clearTimeout(timer); }, [load]);
  useEffect(() => {
    if (!editable || searchParams.get("new") !== "1") return;
    setEditing(null);
    setModal(true);
    const next = new URLSearchParams(searchParams);
    next.delete("new");
    setSearchParams(next, { replace: true });
  }, [editable, searchParams, setSearchParams]);

  async function save(values) {
    const cleaned = Object.fromEntries(Object.entries(values).filter(([, value]) =>
      !(typeof value === "number" && Number.isNaN(value)) && !(value instanceof FileList && value.length === 0)
    ));
    const hasFile = fields.some((field) => field.type === "file" && cleaned[field.name]?.[0]);
    let payload = cleaned;
    if (hasFile) { payload = new FormData(); Object.entries(cleaned).forEach(([key, val]) => { if (val !== "" && val != null) payload.append(key, val?.[0] instanceof File ? val[0] : val); }); }
    if (editing) await api.patch(`${endpoint}${editing.id}/`, payload); else await api.post(endpoint, payload);
    toast.success(`${title.replace(/s$/, "")} saved.`); setModal(false); setEditing(null); await load();
  }
  async function remove(row) {
    if (!window.confirm("Are you sure? This action may archive the record.")) return;
    try { await api.delete(`${endpoint}${row.id}/`); toast.success("Record removed."); load(); } catch (err) { toast.error(apiError(err)); }
  }
  return <>{!embedded && <PageHeader title={title} description={description} actions={editable && <button className="btn-primary" onClick={() => { setEditing(null); setModal(true); }}><Plus />Add new</button>} />}{embedded && editable && <div className="mb-4 flex justify-end"><button className="btn-primary" onClick={() => { setEditing(null); setModal(true); }}><Plus />Add new</button></div>}
    <section className="card overflow-hidden"><div className="border-b p-4"><div className="relative max-w-md"><Search className="absolute left-3 top-3 h-5 w-5 text-stone-400" /><input className="field pl-10" placeholder={`Search ${title.toLowerCase()}…`} value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} /></div></div>
      <div className="p-4">{loading ? <LoadingScreen /> : error ? <ErrorState message={error} retry={load} /> : <DataTable rows={rows} columns={columns} page={page} pages={Math.max(1, Math.ceil(count / 20))} setPage={setPage} rowActions={rowActions ? (row) => rowActions(row, load) : null} onEdit={editable && !createOnly ? (row) => { setEditing(row); setModal(true); } : null} onDelete={editable && !createOnly && allowDelete ? remove : null} />}</div></section>
    <Modal open={modal} title={`${editing ? "Edit" : "Add"} ${title.replace(/s$/, "")}`} onClose={() => setModal(false)}><DynamicForm fields={fields} initial={editing || {}} onSubmit={save} /></Modal></>;
}
