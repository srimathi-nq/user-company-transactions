import tkinter as tk
from tkinter import ttk, messagebox
from database import SessionLocal, engine
from models import Base
from crud import (
    create_user, get_user, get_all_users, update_user, delete_user,
    create_company, get_company, get_all_companies, update_company, delete_company,
    create_transaction, get_transaction, get_all_transactions,
    get_transactions_by_user, get_transactions_by_company,
    update_transaction, delete_transaction
)
from datetime import date, datetime
from decimal import Decimal


class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User & Company Management System")
        self.root.geometry("1000x700")
        
        # Initialize database
        Base.metadata.create_all(bind=engine)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_user_tab()
        self.create_company_tab()
        self.create_transaction_tab()
    
    # ============ USER TAB ============
    def create_user_tab(self):
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="Users")
        
        # Left side - Form
        form_frame = ttk.LabelFrame(user_frame, text="User Form", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Form fields
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_firstname = ttk.Entry(form_frame, width=30)
        self.user_firstname.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_lastname = ttk.Entry(form_frame, width=30)
        self.user_lastname.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_dob = ttk.Entry(form_frame, width=30)
        self.user_dob.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.user_address = ttk.Entry(form_frame, width=30)
        self.user_address.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Balance:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.user_balance = ttk.Entry(form_frame, width=30)
        self.user_balance.grid(row=4, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="User ID (for Update/Delete):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.user_id_entry = ttk.Entry(form_frame, width=30)
        self.user_id_entry.grid(row=5, column=1, pady=5, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Create", command=self.create_user_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Read", command=self.read_user_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_user_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_user_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        
        # Right side - Data display
        display_frame = ttk.LabelFrame(user_frame, text="Users List", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for users
        columns = ("ID", "First Name", "Last Name", "DOB", "Address", "Balance")
        self.user_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_users()
    
    def create_user_action(self):
        try:
            db = SessionLocal()
            dob = date.fromisoformat(self.user_dob.get())
            balance = Decimal(self.user_balance.get() or '0.00')
            
            user = create_user(
                db=db,
                firstname=self.user_firstname.get(),
                lastname=self.user_lastname.get(),
                date_of_birth=dob,
                address=self.user_address.get(),
                balance=balance
            )
            messagebox.showinfo("Success", f"User created: {user.user_id}")
            db.close()
            self.clear_user_form()
            self.refresh_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")
    
    def read_user_action(self):
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showwarning("Warning", "Please enter User ID")
            return
        
        try:
            db = SessionLocal()
            user = get_user(db, user_id)
            db.close()
            
            if user:
                self.user_firstname.delete(0, tk.END)
                self.user_firstname.insert(0, user.firstname)
                self.user_lastname.delete(0, tk.END)
                self.user_lastname.insert(0, user.lastname)
                self.user_dob.delete(0, tk.END)
                self.user_dob.insert(0, str(user.date_of_birth))
                self.user_address.delete(0, tk.END)
                self.user_address.insert(0, user.address)
                self.user_balance.delete(0, tk.END)
                self.user_balance.insert(0, str(user.balance))
                messagebox.showinfo("Success", f"User found: {user.user_id}")
            else:
                messagebox.showinfo("Not Found", "User not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read user: {str(e)}")
    
    def update_user_action(self):
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showwarning("Warning", "Please enter User ID")
            return
        
        try:
            db = SessionLocal()
            dob = date.fromisoformat(self.user_dob.get()) if self.user_dob.get() else None
            balance = Decimal(self.user_balance.get()) if self.user_balance.get() else None
            
            user = update_user(
                db=db,
                user_id=user_id,
                firstname=self.user_firstname.get() or None,
                lastname=self.user_lastname.get() or None,
                date_of_birth=dob,
                address=self.user_address.get() or None,
                balance=balance
            )
            db.close()
            
            if user:
                messagebox.showinfo("Success", f"User updated: {user.user_id}")
                self.clear_user_form()
                self.refresh_users()
            else:
                messagebox.showwarning("Warning", "User not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")
    
    def delete_user_action(self):
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showwarning("Warning", "Please enter User ID")
            return
        
        try:
            db = SessionLocal()
            # Check if user has transactions
            from crud import get_transactions_by_user
            transactions = get_transactions_by_user(db, user_id)
            warning_msg = f"Delete user {user_id}?"
            if transactions:
                warning_msg += f"\n\nWARNING: This user has {len(transactions)} transaction(s) that will also be deleted."
            
            if not messagebox.askyesno("Confirm Deletion", warning_msg):
                db.close()
                return
            
            if delete_user(db, user_id):
                msg = f"User {user_id} deleted"
                if transactions:
                    msg += f"\n{len(transactions)} related transaction(s) were also deleted."
                messagebox.showinfo("Success", msg)
                self.clear_user_form()
                self.refresh_users()
                # Refresh transactions tab if it exists
                if hasattr(self, 'refresh_transactions'):
                    self.refresh_transactions()
            else:
                messagebox.showwarning("Warning", "User not found")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
    
    def refresh_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        try:
            db = SessionLocal()
            users = get_all_users(db)
            db.close()
            
            for user in users:
                self.user_tree.insert("", tk.END, values=(
                    user.user_id,
                    user.firstname,
                    user.lastname,
                    str(user.date_of_birth),
                    user.address,
                    f"${user.balance}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh users: {str(e)}")
    
    def clear_user_form(self):
        self.user_firstname.delete(0, tk.END)
        self.user_lastname.delete(0, tk.END)
        self.user_dob.delete(0, tk.END)
        self.user_address.delete(0, tk.END)
        self.user_balance.delete(0, tk.END)
        self.user_id_entry.delete(0, tk.END)
    
    # ============ COMPANY TAB ============
    def create_company_tab(self):
        company_frame = ttk.Frame(self.notebook)
        self.notebook.add(company_frame, text="Companies")
        
        # Left side - Form
        form_frame = ttk.LabelFrame(company_frame, text="Company Form", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Form fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.company_name = ttk.Entry(form_frame, width=30)
        self.company_name.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.company_location = ttk.Entry(form_frame, width=30)
        self.company_location.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Company ID (for Update/Delete):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.company_id_entry = ttk.Entry(form_frame, width=30)
        self.company_id_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Create", command=self.create_company_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Read", command=self.read_company_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_company_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_company_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_companies).pack(side=tk.LEFT, padx=5)
        
        # Right side - Data display
        display_frame = ttk.LabelFrame(company_frame, text="Companies List", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for companies
        columns = ("ID", "Name", "Location")
        self.company_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.company_tree.heading(col, text=col)
            self.company_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.company_tree.yview)
        self.company_tree.configure(yscrollcommand=scrollbar.set)
        
        self.company_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_companies()
    
    def create_company_action(self):
        try:
            db = SessionLocal()
            company = create_company(
                db=db,
                name=self.company_name.get(),
                location=self.company_location.get()
            )
            messagebox.showinfo("Success", f"Company created: {company.company_id}")
            db.close()
            self.clear_company_form()
            self.refresh_companies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create company: {str(e)}")
    
    def read_company_action(self):
        company_id = self.company_id_entry.get()
        if not company_id:
            messagebox.showwarning("Warning", "Please enter Company ID")
            return
        
        try:
            db = SessionLocal()
            company = get_company(db, company_id)
            db.close()
            
            if company:
                self.company_name.delete(0, tk.END)
                self.company_name.insert(0, company.name)
                self.company_location.delete(0, tk.END)
                self.company_location.insert(0, company.location)
                messagebox.showinfo("Success", f"Company found: {company.company_id}")
            else:
                messagebox.showinfo("Not Found", "Company not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read company: {str(e)}")
    
    def update_company_action(self):
        company_id = self.company_id_entry.get()
        if not company_id:
            messagebox.showwarning("Warning", "Please enter Company ID")
            return
        
        try:
            db = SessionLocal()
            company = update_company(
                db=db,
                company_id=company_id,
                name=self.company_name.get() or None,
                location=self.company_location.get() or None
            )
            db.close()
            
            if company:
                messagebox.showinfo("Success", f"Company updated: {company.company_id}")
                self.clear_company_form()
                self.refresh_companies()
            else:
                messagebox.showwarning("Warning", "Company not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update company: {str(e)}")
    
    def delete_company_action(self):
        company_id = self.company_id_entry.get()
        if not company_id:
            messagebox.showwarning("Warning", "Please enter Company ID")
            return
        
        try:
            db = SessionLocal()
            # Check if company has transactions
            from crud import get_transactions_by_company
            transactions = get_transactions_by_company(db, company_id)
            warning_msg = f"Delete company {company_id}?"
            if transactions:
                warning_msg += f"\n\nWARNING: This company has {len(transactions)} transaction(s) that will also be deleted."
            
            if not messagebox.askyesno("Confirm Deletion", warning_msg):
                db.close()
                return
            
            if delete_company(db, company_id):
                msg = f"Company {company_id} deleted"
                if transactions:
                    msg += f"\n{len(transactions)} related transaction(s) were also deleted."
                messagebox.showinfo("Success", msg)
                self.clear_company_form()
                self.refresh_companies()
                # Refresh transactions tab if it exists
                if hasattr(self, 'refresh_transactions'):
                    self.refresh_transactions()
            else:
                messagebox.showwarning("Warning", "Company not found")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete company: {str(e)}")
    
    def refresh_companies(self):
        for item in self.company_tree.get_children():
            self.company_tree.delete(item)
        
        try:
            db = SessionLocal()
            companies = get_all_companies(db)
            db.close()
            
            for company in companies:
                self.company_tree.insert("", tk.END, values=(
                    company.company_id,
                    company.name,
                    company.location
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh companies: {str(e)}")
    
    def clear_company_form(self):
        self.company_name.delete(0, tk.END)
        self.company_location.delete(0, tk.END)
        self.company_id_entry.delete(0, tk.END)
    
    # ============ TRANSACTION TAB ============
    def create_transaction_tab(self):
        transaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(transaction_frame, text="Transactions")
        
        # Left side - Form
        form_frame = ttk.LabelFrame(transaction_frame, text="Transaction Form", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Form fields
        ttk.Label(form_frame, text="User ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.trans_user_id = ttk.Entry(form_frame, width=30)
        self.trans_user_id.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Company ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.trans_company_id = ttk.Entry(form_frame, width=30)
        self.trans_company_id.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Number of Shares:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.trans_shares = ttk.Entry(form_frame, width=30)
        self.trans_shares.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="DateTime (YYYY-MM-DD HH:MM:SS):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.trans_datetime = ttk.Entry(form_frame, width=30)
        self.trans_datetime.grid(row=3, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="(Leave empty for current time)").grid(row=4, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(form_frame, text="Transaction ID (for Update/Delete):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.trans_id_entry = ttk.Entry(form_frame, width=30)
        self.trans_id_entry.grid(row=5, column=1, pady=5, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Create", command=self.create_transaction_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Read", command=self.read_transaction_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_transaction_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_transaction_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)
        
        # Right side - Data display
        display_frame = ttk.LabelFrame(transaction_frame, text="Transactions List", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for transactions
        columns = ("ID", "User ID", "Company ID", "Shares", "DateTime")
        self.transaction_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_transactions()
    
    def create_transaction_action(self):
        try:
            db = SessionLocal()
            trans_datetime = None
            if self.trans_datetime.get():
                trans_datetime = datetime.strptime(self.trans_datetime.get(), "%Y-%m-%d %H:%M:%S")
            
            transaction = create_transaction(
                db=db,
                user_id=self.trans_user_id.get(),
                company_id=self.trans_company_id.get(),
                number_of_shares=int(self.trans_shares.get()),
                transaction_datetime=trans_datetime
            )
            messagebox.showinfo("Success", f"Transaction created: ID {transaction.transaction_id}")
            db.close()
            self.clear_transaction_form()
            self.refresh_transactions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create transaction: {str(e)}")
    
    def read_transaction_action(self):
        trans_id = self.trans_id_entry.get()
        if not trans_id:
            messagebox.showwarning("Warning", "Please enter Transaction ID")
            return
        
        try:
            db = SessionLocal()
            transaction = get_transaction(db, trans_id)
            db.close()
            
            if transaction:
                self.trans_user_id.delete(0, tk.END)
                self.trans_user_id.insert(0, transaction.user_id)
                self.trans_company_id.delete(0, tk.END)
                self.trans_company_id.insert(0, transaction.company_id)
                self.trans_shares.delete(0, tk.END)
                self.trans_shares.insert(0, str(transaction.number_of_shares))
                self.trans_datetime.delete(0, tk.END)
                self.trans_datetime.insert(0, transaction.transaction_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                messagebox.showinfo("Success", f"Transaction found: ID {transaction.transaction_id}")
            else:
                messagebox.showinfo("Not Found", "Transaction not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read transaction: {str(e)}")
    
    def update_transaction_action(self):
        trans_id = self.trans_id_entry.get()
        if not trans_id:
            messagebox.showwarning("Warning", "Please enter Transaction ID")
            return
        
        try:
            db = SessionLocal()
            trans_datetime = None
            if self.trans_datetime.get():
                trans_datetime = datetime.strptime(self.trans_datetime.get(), "%Y-%m-%d %H:%M:%S")
            
            transaction = update_transaction(
                db=db,
                transaction_id=trans_id,
                user_id=self.trans_user_id.get() or None,
                company_id=self.trans_company_id.get() or None,
                number_of_shares=int(self.trans_shares.get()) if self.trans_shares.get() else None,
                transaction_datetime=trans_datetime
            )
            db.close()
            
            if transaction:
                messagebox.showinfo("Success", f"Transaction updated: ID {transaction.transaction_id}")
                self.clear_transaction_form()
                self.refresh_transactions()
            else:
                messagebox.showwarning("Warning", "Transaction not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update transaction: {str(e)}")
    
    def delete_transaction_action(self):
        trans_id = self.trans_id_entry.get()
        if not trans_id:
            messagebox.showwarning("Warning", "Please enter Transaction ID")
            return
        
        if not messagebox.askyesno("Confirm", f"Delete transaction {trans_id}?"):
            return
        
        try:
            db = SessionLocal()
            if delete_transaction(db, trans_id):
                messagebox.showinfo("Success", f"Transaction {trans_id} deleted")
                self.clear_transaction_form()
                self.refresh_transactions()
            else:
                messagebox.showwarning("Warning", "Transaction not found")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")
    
    def refresh_transactions(self):
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        try:
            db = SessionLocal()
            transactions = get_all_transactions(db)
            db.close()
            
            for trans in transactions:
                self.transaction_tree.insert("", tk.END, values=(
                    trans.transaction_id,
                    trans.user_id,
                    trans.company_id,
                    trans.number_of_shares,
                    trans.transaction_datetime.strftime("%Y-%m-%d %H:%M:%S")
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh transactions: {str(e)}")
    
    def clear_transaction_form(self):
        self.trans_user_id.delete(0, tk.END)
        self.trans_company_id.delete(0, tk.END)
        self.trans_shares.delete(0, tk.END)
        self.trans_datetime.delete(0, tk.END)
        self.trans_id_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

