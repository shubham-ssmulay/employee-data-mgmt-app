import React, { useEffect, useState } from "react";

const API = "/api/employees";
const POSITION_OPTIONS = [
  "Software Engineer",
  "Data Engineer",
  "ML Engineer",
  "Quality Analyst",
  "Solutions Architect",
  "Sales Representative"
];


export default function App() {
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState({ name: "", email: "", position: "" });
  const [editing, setEditing] = useState(null);
  const [errors, setErrors] = useState({});
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);

  // Fetch employees
  async function fetchList(q = "") {
    const res = await fetch(`${API}${q ? `?q=${q}` : ""}`);
    const data = await res.json();
    setEmployees(data);
  }

  useEffect(() => {
    fetchList();
  }, []);

  // Form submit handler with validation
  async function onSubmit(e) {
    e.preventDefault();
    setErrors({}); // reset

    // Client-side validation
    let newErrors = {};
    if (!form.name.trim()) newErrors.name = "Name is required";
    else if (form.name.length < 3) newErrors.name = "Name must be at least 3 characters";

    if (!form.email.trim()) newErrors.email = "Email is required";
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) newErrors.email = "Invalid email format";

    if (!form.position.trim()) newErrors.position = "Position is required";
    else if (form.position.length < 2) newErrors.position = "Position must be at least 2 characters";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const method = editing ? "PUT" : "POST";
    const url = editing ? `${API}/${editing.id}` : API;

    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    if (!res.ok) {
      const data = await res.json();
      // Show backend error (e.g. duplicate email)
      setErrors({ api: data.detail || "Something went wrong" });
      return;
    }

    // Success: reset form
    setForm({ name: "", email: "", position: "" });
    setEditing(null);
    setShowModal(false);
    fetchList(search);
  }

  // Soft delete
  async function onDelete(id) {
    if (!confirm("Delete this employee?")) return;
    const res = await fetch(`${API}/${id}`, { method: "DELETE" });
    if (res.ok) fetchList(search);
  }

  // Restore soft deleted employee
  async function onRestore(id) {
    const res = await fetch(`${API}/${id}/restore`, { method: "POST" });
    if (res.ok) fetchList(search);
  }

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Employee Management System</h1>

      {/* Search + Add button */}
      <div className="mb-4 flex gap-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchList(search);
          }}
          className="flex gap-2 flex-1"
        >
          <input
            className="border px-2 py-1 flex-1 rounded"
            placeholder="Search by name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="bg-blue-600 text-white px-3 py-1 rounded" type="submit">
            Search
          </button>
          <button
            className="bg-gray-300 px-3 py-1 rounded"
            type="button"
            onClick={() => {
              setSearch("");
              fetchList();
            }}
          >
            Clear
          </button>
        </form>

        <button
          onClick={() => {
            setEditing(null);
            setForm({ name: "", email: "", position: "" });
            setErrors({});
            setShowModal(true);
          }}
          className="bg-green-600 text-white px-3 py-1 rounded"
        >
          + Add Employee
        </button>
      </div>

      {/* Employee Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse bg-white shadow">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2 text-left">Name</th>
              <th className="border p-2 text-left">Email</th>
              <th className="border p-2 text-left">Position</th>
              <th className="border p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td className="border p-2">{emp.name}</td>
                <td className="border p-2">{emp.email}</td>
                <td className="border p-2">{emp.position}</td>
                <td className="border p-2 flex gap-2">
                  {emp.is_active ? (
                    <>
                      <button
                        onClick={() => {
                          setEditing(emp);
                          setForm({ name: emp.name, email: emp.email, position: emp.position });
                          setErrors({});
                          setShowModal(true);
                        }}
                        className="bg-yellow-500 text-white px-2 py-1 rounded"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => onDelete(emp.id)}
                        className="bg-red-600 text-white px-2 py-1 rounded"
                      >
                        Delete
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => onRestore(emp.id)}
                      className="bg-green-500 text-white px-2 py-1 rounded"
                    >
                      Restore
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white rounded-lg shadow-lg w-96 p-6 relative">
            <h2 className="text-xl font-semibold mb-4">
              {editing ? "Edit Employee" : "Add Employee"}
            </h2>

            {/* API error */}
            {errors.api && (
              <div className="text-red-600 text-sm mb-2">{errors.api}</div>
            )}

            <form onSubmit={onSubmit} className="space-y-3">
              <div>
                <label className="block font-medium" htmlFor="name">Name</label>
                <input
                  id="name"
                  className="border px-2 py-1 w-full rounded"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
                {errors.name && <div className="text-red-500 text-sm">{errors.name}</div>}
              </div>

              <div>
                <label className="block font-medium" htmlFor="email">Email</label>
                <input
                  id="email"
                  className="border px-2 py-1 w-full rounded"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
                {errors.email && <div className="text-red-500 text-sm" role="alert">{errors.email}</div>}
              </div>

              <div>
                <label className="block font-medium" htmlFor="position">Position</label>
                <select
                  id="position"
                  className="border px-2 py-1 w-full rounded"
                  value={form.position}
                  onChange={(e) => setForm({ ...form, position: e.target.value })}
                >
                  <option value="">-- Select Position --</option>
                  {POSITION_OPTIONS.map((pos) => (
                    <option key={pos} value={pos}>
                      {pos}
                    </option>
                  ))}
                </select>
                {errors.position && <div className="text-red-500 text-sm" role="alert">{errors.position}</div>}
              </div>

              <div className="flex justify-end gap-2 mt-3">
                <button
                  type="button"
                  onClick={() => {
                    setEditing(null);
                    setForm({ name: "", email: "", position: "" });
                    setErrors({});
                    setShowModal(false);
                  }}
                  className="bg-gray-400 px-3 py-1 rounded hover:bg-gray-500 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition"
                >
                  {editing ? "Save" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
