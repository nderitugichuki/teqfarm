import { useState } from "react";
import { Download, FileSpreadsheet, FileText, LoaderCircle } from "lucide-react";
import { toast } from "sonner";
import PageHeader from "../../components/ui/PageHeader";
import { api, apiError } from "../../lib/api";

const reports = [["daily", "Daily report"], ["weekly", "Weekly report"], ["monthly", "Monthly report"], ["production", "Egg production"], ["mortality", "Mortality"], ["feed", "Feed consumption"], ["sales", "Sales"], ["expenses", "Expenses"], ["profit-loss", "Profit & loss"], ["inventory", "Inventory"]];
export default function ReportsPage() {
  const today = new Date().toISOString().slice(0, 10);
  const [filters, setFilters] = useState({ start: today.slice(0, 8) + "01", end: today });
  const [downloading, setDownloading] = useState("");
  async function download(type, format) {
    const key = `${type}-${format}`; setDownloading(key);
    try { const { data } = await api.get(`/reports/${type}/`, { params: { ...filters, format }, responseType: "blob" });
      const url = URL.createObjectURL(data); const anchor = document.createElement("a"); anchor.href = url; anchor.download = `teqfarm-${type}.${format}`; anchor.click(); URL.revokeObjectURL(url);
    } catch (error) { toast.error(apiError(error)); } finally { setDownloading(""); }
  }
  return <><PageHeader title="Reports" description="Operational and financial reports ready for review or export." />
    <section className="card mb-6 grid gap-4 p-4 sm:grid-cols-2 sm:p-5"><label><span className="label">From</span><input className="field" type="date" value={filters.start} onChange={(e) => setFilters({ ...filters, start: e.target.value })} /></label><label><span className="label">To</span><input className="field" type="date" value={filters.end} onChange={(e) => setFilters({ ...filters, end: e.target.value })} /></label></section>
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{reports.map(([type, label]) => <article key={type} className="card p-5"><div className="flex items-center gap-3"><span className="rounded-xl bg-farm-50 p-3 text-farm-700"><FileText /></span><h2 className="font-bold">{label}</h2></div><div className="mt-5 grid grid-cols-2 gap-2"><button onClick={() => download(type, "pdf")} className="btn-secondary">{downloading === `${type}-pdf` ? <LoaderCircle className="animate-spin" /> : <Download />}PDF</button><button onClick={() => download(type, "xlsx")} className="btn-secondary">{downloading === `${type}-xlsx` ? <LoaderCircle className="animate-spin" /> : <FileSpreadsheet />}Excel</button></div></article>)}</section>
  </>;
}

