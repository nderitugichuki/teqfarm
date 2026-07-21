import { render, screen } from "@testing-library/react";
import DataTable from "./DataTable";

test("renders farm records in the table", () => {
  render(<DataTable rows={[{ id: 1, batch: "TF-001", birds: 120 }]} columns={[
    { key: "batch", label: "Batch" }, { key: "birds", label: "Birds" },
  ]} page={1} pages={1} setPage={() => {}} />);
  expect(screen.getAllByText("TF-001").length).toBeGreaterThan(0);
  expect(screen.getAllByText("120").length).toBeGreaterThan(0);
});

