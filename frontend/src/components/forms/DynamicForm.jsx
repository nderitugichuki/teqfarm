import { useEffect, useMemo, useState } from "react";
import { LoaderCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { api, apiError, results } from "../../lib/api";

function RemoteSelect({ field, register, error }) {
  const [options, setOptions] = useState([]);
  useEffect(() => { api.get(field.optionsEndpoint, { params: { page_size: 100 } }).then(({ data }) => setOptions(results(data))).catch(() => {}); }, [field.optionsEndpoint]);
  return <><select className="field" {...register(field.name, { required: field.required })}><option value="">Select {field.label.toLowerCase()}</option>{options.map((item) =>
    <option key={item.id} value={item.id}>{field.optionLabel ? field.optionLabel(item) : item.name || item.batch_code || item.sku}</option>)}</select>{error && <p className="mt-1 text-xs text-red-600">This field is required.</p>}</>;
}

export default function DynamicForm({ fields, initial, onSubmit, submitLabel = "Save" }) {
  const defaultValues = useMemo(() => Object.fromEntries(Object.entries(initial || {}).filter(([key]) => fields.find((field) => field.name === key)?.type !== "file")), [fields, initial]);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({ defaultValues });
  const [serverError, setServerError] = useState("");
  useEffect(() => { reset(defaultValues); }, [defaultValues, reset]);
  async function submit(values) {
    setServerError("");
    try { await onSubmit(values); } catch (error) { setServerError(apiError(error)); }
  }
  return <form onSubmit={handleSubmit(submit)} className="space-y-5">{serverError && <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{serverError}</div>}
    <div className="grid gap-4 sm:grid-cols-2">{fields.map((field) => <label key={field.name} className={field.full ? "sm:col-span-2" : ""}>
      <span className="label">{field.label}{field.required && <span className="text-red-500"> *</span>}</span>
      {field.type === "remote" ? <RemoteSelect field={field} register={register} error={errors[field.name]} /> : field.type === "select" ?
        <select className="field" {...register(field.name, { required: field.required })}><option value="">Select {field.label.toLowerCase()}</option>{field.options.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select> :
      field.type === "textarea" ? <textarea rows="4" className="field" {...register(field.name, { required: field.required })} /> :
      field.type === "file" ? <input className="field pt-2" type="file" accept={field.accept} {...register(field.name)} /> :
        <input className="field" type={field.type || "text"} step={field.step} min={field.min} {...register(field.name, { required: field.required, valueAsNumber: field.type === "number" })} />}
      {field.type !== "remote" && errors[field.name] && <p className="mt-1 text-xs text-red-600">This field is required.</p>}
    </label>)}</div>
    <button className="btn-primary w-full sm:w-auto" disabled={isSubmitting}>{isSubmitting && <LoaderCircle className="h-5 w-5 animate-spin" />}{submitLabel}</button>
  </form>;
}
