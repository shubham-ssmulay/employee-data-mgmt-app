import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import App from "../App";

// -----------------------------
// Set up modal root (for portal modals)
// -----------------------------
beforeAll(() => {
  const modalRoot = document.createElement("div");
  modalRoot.setAttribute("id", "modal-root");
  document.body.appendChild(modalRoot);
});

afterAll(() => {
  document.body.innerHTML = "";
});

// -----------------------------
// Mock fetch API
// -----------------------------
beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve([
          { id: 1, name: "Alice", email: "alice@test.com", position: "Dev", is_active: true },
        ]),
    })
  );
});

afterEach(() => {
  jest.resetAllMocks();
});

// -----------------------------
// Tests
// -----------------------------

test("renders employee table with fetched employees", async () => {
  render(<App />);

  expect(screen.getByText(/Employee Management System/i)).toBeInTheDocument();

  // Wait for table data to appear
  await waitFor(() => {
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });
});

test("shows modal when Add Employee button is clicked", async () => {
  render(<App />);

  fireEvent.click(screen.getByText("+ Add Employee"));

  // Wait for modal and inputs to appear
  await waitFor(() => {
    expect(screen.getByRole("heading", { name: "Add Employee" })).toBeInTheDocument();
    expect(screen.getByLabelText("Name")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Position")).toBeInTheDocument();
  });
});

test("shows validation errors for empty form fields", async () => {
  render(<App />);

  fireEvent.click(screen.getByText("+ Add Employee"));
  fireEvent.click(screen.getByText("Create"));

  await waitFor(() => {
    expect(screen.getByText("Name is required")).toBeInTheDocument();
    expect(screen.getByText("Email is required")).toBeInTheDocument();
    expect(screen.getByText("Position is required")).toBeInTheDocument();
  });
});


test("closes modal on cancel", async () => {
  render(<App />);

  fireEvent.click(screen.getByText("+ Add Employee"));
  fireEvent.click(screen.getByText("Cancel"));

  await waitFor(() => {
    expect(screen.queryByRole("heading", { name: "Add Employee" })).not.toBeInTheDocument();
  });
});
