import { Inbox, LoaderCircle } from "lucide-react";

export function LoadingScreen() { return <div className="grid min-h-[50vh] place-items-center"><LoaderCircle className="h-8 w-8 animate-spin text-farm-600" /></div>; }
export function EmptyState({ message = "No records found." }) { return <div className="grid place-items-center py-14 text-center text-stone-500"><Inbox className="mb-3 h-9 w-9" /><p>{message}</p></div>; }
export function ErrorState({ message, retry }) { return <div className="card p-8 text-center"><p className="text-red-700">{message}</p>{retry && <button onClick={retry} className="btn-secondary mt-4">Try again</button>}</div>; }

