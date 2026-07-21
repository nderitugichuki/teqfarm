export default function PageHeader({ title, description, actions }) {
  return <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><h1 className="text-2xl font-bold tracking-tight sm:text-3xl">{title}</h1>{description && <p className="mt-1 text-sm text-stone-500">{description}</p>}</div>{actions && <div className="flex gap-2">{actions}</div>}</div>;
}

