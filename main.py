import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkFont
from collections import deque
import copy

class OSProcessCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OS Process Management Calculator")
        self.root.geometry("1200x800")
        
        # Configure styles first
        self.setup_styles()
        
        # Now we can use self.colors
        self.root.configure(bg=self.colors['primary'])
        
        # Initialize variables
        self.processes = []
        self.results = []
        self.current_algorithm = tk.StringVar(value="FCFS")
        self.time_quantum = tk.StringVar(value="2")
        self.num_processes = tk.StringVar(value="3")
        
        self.create_main_interface()
        self.root.mainloop()
    
    def setup_styles(self):
        """Setup consistent styling for the application"""
        self.colors = {
            'primary': '#1e1e1e',      # Dark background
            'secondary': '#007acc',     # Bright blue for buttons
            'success': '#28a745',      # Green for success actions
            'warning': '#ffc107',      # Yellow for warnings
            'danger': '#dc3545',       # Red for errors
            'light': '#2d2d2d',        # Slightly lighter than primary
            'dark': '#151515',         # Darker shade for contrast
            'white': '#ffffff',        # White for text
            'gray': '#6c757d',         # Gray for subtle elements
            'highlight': '#3c3c3c',    # Highlight color for selected items
            'border': '#404040'        # Border color
        }
        
        self.fonts = {
            'title': tkFont.Font(family="Segoe UI", size=16, weight="bold"),
            'heading': tkFont.Font(family="Segoe UI", size=12, weight="bold"),
            'body': tkFont.Font(family="Segoe UI", size=10),
            'small': tkFont.Font(family="Segoe UI", size=9)
        }
    
    def create_main_interface(self):
        """Create the main interface layout"""
        # Title Header
        self.create_header()
        
        # Main container with padding
        self.main_container = tk.Frame(self.root, bg='#000000')  # Changed to black
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configuration Panel (Left Side)
        self.create_config_panel()
        
        # Results Panel (Right Side)
        self.create_results_panel()
    
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Operating System Process Management Calculator",
            font=self.fonts['title'],
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="CPU Scheduling Algorithms Simulator",
            font=self.fonts['body'],
            fg=self.colors['gray'],
            bg=self.colors['dark']
        )
        subtitle_label.pack()
    
    def create_config_panel(self):
        """Create configuration panel on the left side"""
        left_panel = tk.Frame(
            self.main_container, 
            bg=self.colors['light'],
            relief=tk.RAISED,
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_panel.configure(width=400)
        
        # Algorithm Selection Section
        self.create_algorithm_section(left_panel)
        
        # Process Configuration Section
        self.create_process_config_section(left_panel)
        
        # Process Input Section
        self.create_process_input_section(left_panel)
    
    def create_algorithm_section(self, parent):
        """Create algorithm selection section"""
        algo_frame = tk.LabelFrame(
            parent,
            text="Algorithm Selection",
            font=self.fonts['heading'],
            fg=self.colors['white'],  # Changed to white for better visibility
            bg=self.colors['dark'],   # Changed to dark background
            padx=15,
            pady=10
        )
        algo_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        algorithms = [
            ("First Come First Serve (FCFS)", "FCFS"),
            ("Shortest Job First (SJF)", "SJF"),
            ("Shortest Remaining Time First (SRTF)", "SRTF"),
            ("Round Robin (RR)", "RR"),
            ("Priority (Preemptive)", "Priority_Preemptive"),
            ("Priority (Non-Preemptive)", "Priority_NonPreemptive")
        ]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.current_algorithm,
                value=value,
                font=self.fonts['body'],
                bg=self.colors['dark'],
                fg=self.colors['white'],
                selectcolor=self.colors['primary'],
                activebackground=self.colors['dark'],
                activeforeground=self.colors['secondary'],
                command=self.on_algorithm_change
            )
            rb.pack(anchor=tk.W, pady=5)  # Increased padding
        
        # Time Quantum for Round Robin
        self.quantum_frame = tk.Frame(algo_frame, bg=self.colors['white'])
        self.quantum_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            self.quantum_frame,
            text="Time Quantum:",
            font=self.fonts['body'],
            bg=self.colors['white']
        ).pack(side=tk.LEFT)
        
        self.quantum_entry = tk.Entry(
            self.quantum_frame,
            textvariable=self.time_quantum,
            width=10,
            font=self.fonts['body']
        )
        self.quantum_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        self.quantum_frame.pack_forget()  # Initially hidden
    
    def create_process_config_section(self, parent):
        """Create process configuration section"""
        config_frame = tk.LabelFrame(
            parent,
            text="Process Configuration",
            font=self.fonts['heading'],
            fg=self.colors['white'],
            bg=self.colors['dark'],
            padx=15,
            pady=10
        )
        config_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Number of processes
        num_frame = tk.Frame(config_frame, bg=self.colors['dark'])
        num_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            num_frame,
            text="Number of Processes:",
            font=self.fonts['body'],
            fg=self.colors['white'],
            bg=self.colors['dark']
        ).pack(side=tk.LEFT)
        
        num_spinbox = tk.Spinbox(
            num_frame,
            from_=1,
            to=10,
            textvariable=self.num_processes,
            width=10,
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['white'],
            buttonbackground=self.colors['secondary'],
            relief=tk.FLAT
        )
        num_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Generate button with improved styling
        generate_btn = tk.Button(
            config_frame,
            text="Generate Process Table",
            command=self.generate_process_table,
            font=self.fonts['body'],
            bg=self.colors['secondary'],
            fg=self.colors['dark'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['white'],
            padx=20,
            pady=5,
            cursor='hand2',
            relief=tk.FLAT
        )
        generate_btn.pack(pady=(10, 0))
    
    def create_process_input_section(self, parent):
        """Create process input section"""
        self.input_frame = tk.LabelFrame(
            parent,
            text="Process Details",
            font=self.fonts['heading'],
            fg=self.colors['white'],
            bg=self.colors['dark'],
            padx=15,
            pady=10
        )
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # This will be populated when generate button is clicked
        self.process_entries = []
        
        # Add placeholder text
        placeholder = tk.Label(
            self.input_frame,
            text="Click 'Generate Process Table' to start",
            font=self.fonts['body'],
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        placeholder.pack(expand=True, pady=20)
    
    def create_results_panel(self):
        """Create results panel on the right side"""
        self.results_panel = tk.Frame(
            self.main_container, 
            bg=self.colors['dark'],  # Changed to dark theme
            relief=tk.RAISED, 
            bd=1
        )
        self.results_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results header
        results_header = tk.Label(
            self.results_panel,
            text="Calculation Results",
            font=self.fonts['heading'],
            fg=self.colors['white'],  # Changed to white for visibility
            bg=self.colors['dark']   # Changed to dark theme
        )
        results_header.pack(pady=(15, 10))
        
        # Placeholder for results
        self.results_content = tk.Frame(
            self.results_panel, 
            bg=self.colors['dark']  # Changed to dark theme
        )
        self.results_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        placeholder = tk.Label(
            self.results_content,
            text="Configure processes and click 'Calculate' to see results",
            font=self.fonts['body'],
            fg=self.colors['white'],  # Changed to white for visibility
            bg=self.colors['dark']   # Changed to dark theme
        )
        placeholder.pack(expand=True)
    
    def on_algorithm_change(self):
        """Handle algorithm selection change"""
        if self.current_algorithm.get() == "RR":
            self.quantum_frame.pack(fill=tk.X, pady=(10, 0))
        else:
            self.quantum_frame.pack_forget()
    
    def generate_process_table(self):
        """Generate process input table"""
        # Clear existing entries
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        try:
            num_proc = int(self.num_processes.get())
            if num_proc <= 0 or num_proc > 10:
                raise ValueError("Number of processes must be between 1 and 10")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid number of processes: {e}")
            return
        
        # Create table headers
        headers = ["Process", "Arrival Time", "Burst Time"]
        if "Priority" in self.current_algorithm.get():
            headers.append("Priority")
        
        # Create header row
        header_frame = tk.Frame(self.input_frame, bg=self.colors['light'])
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        for col, header in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=header,
                font=self.fonts['heading'],
                bg=self.colors['light'],
                fg=self.colors['primary'],
                width=12,
                relief=tk.RIDGE,
                bd=1
            )
            label.grid(row=0, column=col, padx=1, pady=1, sticky="ew")
        
        # Create input rows
        self.process_entries = []
        for i in range(num_proc):
            row_frame = tk.Frame(self.input_frame, bg=self.colors['white'])
            row_frame.pack(fill=tk.X, pady=1)
            
            # Process ID (non-editable)
            pid_label = tk.Label(
                row_frame,
                text=f"P{i+1}",
                font=self.fonts['body'],
                bg=self.colors['dark'],
                width=12,
                relief=tk.RIDGE,
                bd=1
            )
            pid_label.grid(row=0, column=0, padx=1, pady=1, sticky="ew")
            
            # Arrival Time
            at_entry = tk.Entry(
                row_frame,
                font=self.fonts['body'],
                bg=self.colors['dark'],
                fg=self.colors['white'],
                insertbackground=self.colors['white'],  # Cursor color
                relief=tk.FLAT,
                highlightbackground=self.colors['border'],
                highlightthickness=1,
                width=12,
                justify='center'
            )
            at_entry.grid(row=0, column=1, padx=1, pady=1, sticky="ew")
            at_entry.insert(0, "0")
            
            # Burst Time
            bt_entry = tk.Entry(
                row_frame,
                font=self.fonts['body'],
                bg=self.colors['dark'],
                fg=self.colors['white'],
                insertbackground=self.colors['white'],  # Cursor color
                relief=tk.FLAT,
                highlightbackground=self.colors['border'],
                highlightthickness=1,
                width=12,
                justify='center'
            )
            bt_entry.grid(row=0, column=2, padx=1, pady=1, sticky="ew")
            bt_entry.insert(0, str((i+1)*2))
            
            entries = [at_entry, bt_entry]
            
            # Priority (if needed)
            if "Priority" in self.current_algorithm.get():
                priority_entry = tk.Entry(
                    row_frame,
                    font=self.fonts['body'],
                    bg=self.colors['dark'],
                    fg=self.colors['white'],
                    insertbackground=self.colors['white'],  # Cursor color
                    relief=tk.FLAT,
                    highlightbackground=self.colors['border'],
                    highlightthickness=1,
                    width=12,
                    justify='center'
                )
                priority_entry.grid(row=0, column=3, padx=1, pady=1, sticky="ew")  # Fixed parenthesis
                priority_entry.insert(0, str(i+1))
                entries.append(priority_entry)
            
            self.process_entries.append(entries)
        
        # Calculate button
        calc_btn = tk.Button(
            self.input_frame,
            text="Calculate Results",
            command=self.calculate_results,
            font=self.fonts['heading'],
            bg=self.colors['success'],
            fg=self.colors['dark'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['white'],
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        calc_btn.pack(pady=(20, 0))
    
    def calculate_results(self):
        """Calculate and display results"""
        try:
            # Validate and collect process data
            processes = []
            for i, entries in enumerate(self.process_entries):
                arrival = int(entries[0].get())
                burst = int(entries[1].get())
                
                if arrival < 0 or burst <= 0:
                    raise ValueError(f"Invalid values for Process P{i+1}")
                
                priority = 0
                if len(entries) > 2:  # Priority included
                    priority = int(entries[2].get())
                
                processes.append({
                    'pid': i + 1,
                    'arrival': arrival,
                    'burst': burst,
                    'priority': priority,
                    'remaining': burst
                })
            
            # Execute selected algorithm
            algorithm = self.current_algorithm.get()
            if algorithm == "FCFS":
                results = self.fcfs(processes)
            elif algorithm == "SJF":
                results = self.sjf(processes)
            elif algorithm == "SRTF":
                results = self.srtf(processes)
            elif algorithm == "RR":
                quantum = int(self.time_quantum.get())
                if quantum <= 0:
                    raise ValueError("Time quantum must be positive")
                results = self.round_robin(processes, quantum)
            elif algorithm == "Priority_Preemptive":
                results = self.priority_preemptive(processes)
            elif algorithm == "Priority_NonPreemptive":
                results = self.priority_non_preemptive(processes)
            
            self.display_results(results, algorithm)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {e}")
    
    def fcfs(self, processes):
        """First Come First Serve algorithm"""
        processes.sort(key=lambda x: x['arrival'])
        current_time = 0
        results = []
        gantt_chart = []
        
        for process in processes:
            start_time = max(current_time, process['arrival'])
            completion_time = start_time + process['burst']
            turnaround_time = completion_time - process['arrival']
            waiting_time = turnaround_time - process['burst']
            
            results.append({
                'pid': process['pid'],
                'arrival': process['arrival'],
                'burst': process['burst'],
                'start': start_time,
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
            
            gantt_chart.append({
                'pid': process['pid'],
                'start': start_time,
                'end': completion_time
            })
            
            current_time = completion_time
        
        return {'results': results, 'gantt': gantt_chart}
    
    def sjf(self, processes):
        """Shortest Job First (Non-preemptive) algorithm"""
        n = len(processes)
        completed = 0
        current_time = 0
        results = []
        gantt_chart = []
        processes_copy = copy.deepcopy(processes)
        
        while completed != n:
            available = [p for p in processes_copy if p['arrival'] <= current_time and p['remaining'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with shortest burst time
            selected = min(available, key=lambda x: x['burst'])
            
            start_time = current_time
            completion_time = current_time + selected['burst']
            turnaround_time = completion_time - selected['arrival']
            waiting_time = turnaround_time - selected['burst']
            
            results.append({
                'pid': selected['pid'],
                'arrival': selected['arrival'],
                'burst': selected['burst'],
                'start': start_time,
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
            
            gantt_chart.append({
                'pid': selected['pid'],
                'start': start_time,
                'end': completion_time
            })
            
            selected['remaining'] = 0
            current_time = completion_time
            completed += 1
        
        return {'results': sorted(results, key=lambda x: x['pid']), 'gantt': gantt_chart}
    
    def srtf(self, processes):
        """Shortest Remaining Time First (Preemptive) algorithm"""
        n = len(processes)
        completed = 0
        current_time = 0
        results = [None] * n
        gantt_chart = []
        processes_copy = copy.deepcopy(processes)
        last_process = None
        
        while completed != n:
            available = [p for p in processes_copy if p['arrival'] <= current_time and p['remaining'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with shortest remaining time
            selected = min(available, key=lambda x: x['remaining'])
            
            # If switching process, record in Gantt chart
            if last_process != selected['pid']:
                if last_process is not None:
                    # Close previous process segment
                    if gantt_chart and gantt_chart[-1]['pid'] == last_process:
                        gantt_chart[-1]['end'] = current_time
                
                gantt_chart.append({
                    'pid': selected['pid'],
                    'start': current_time,
                    'end': current_time + 1
                })
            
            selected['remaining'] -= 1
            
            if selected['remaining'] == 0:
                completion_time = current_time + 1
                turnaround_time = completion_time - selected['arrival']
                waiting_time = turnaround_time - selected['burst']
                
                results[selected['pid'] - 1] = {
                    'pid': selected['pid'],
                    'arrival': selected['arrival'],
                    'burst': selected['burst'],
                    'start': selected['arrival'],  # Will be updated with first start
                    'completion': completion_time,
                    'turnaround': turnaround_time,
                    'waiting': waiting_time
                }
                completed += 1
            
            last_process = selected['pid']
            current_time += 1
        
        # Close last process segment
        if gantt_chart:
            gantt_chart[-1]['end'] = current_time
        
        return {'results': results, 'gantt': gantt_chart}
    
    def round_robin(self, processes, quantum):
        """Round Robin algorithm"""
        n = len(processes)
        queue = deque()
        current_time = 0
        results = [None] * n
        gantt_chart = []
        processes_copy = copy.deepcopy(processes)
        completed = 0
        
        # Add processes that arrive at time 0
        for process in processes_copy:
            if process['arrival'] == 0:
                queue.append(process)
        
        while completed < n:
            if not queue:
                # Find next arriving process
                next_arrival = min([p['arrival'] for p in processes_copy if p['remaining'] > 0])
                current_time = next_arrival
                for process in processes_copy:
                    if process['arrival'] == current_time and process['remaining'] > 0:
                        queue.append(process)
                continue
            
            current_process = queue.popleft()
            
            if current_process['remaining'] > 0:
                # Execute for quantum time or remaining time, whichever is smaller
                execution_time = min(quantum, current_process['remaining'])
                
                gantt_chart.append({
                    'pid': current_process['pid'],
                    'start': current_time,
                    'end': current_time + execution_time
                })
                
                current_process['remaining'] -= execution_time
                current_time += execution_time
                
                # Add newly arrived processes to queue
                for process in processes_copy:
                    if (process['arrival'] <= current_time and 
                        process['remaining'] > 0 and 
                        process not in queue and 
                        process != current_process):
                        queue.append(process)
                
                if current_process['remaining'] == 0:
                    # Process completed
                    completion_time = current_time
                    turnaround_time = completion_time - current_process['arrival']
                    waiting_time = turnaround_time - current_process['burst']
                    
                    results[current_process['pid'] - 1] = {
                        'pid': current_process['pid'],
                        'arrival': current_process['arrival'],
                        'burst': current_process['burst'],
                        'start': current_process['arrival'],
                        'completion': completion_time,
                        'turnaround': turnaround_time,
                        'waiting': waiting_time
                    }
                    completed += 1
                else:
                    # Process not completed, add back to queue
                    queue.append(current_process)
        
        return {'results': results, 'gantt': gantt_chart}
    
    def priority_preemptive(self, processes):
        """Priority Scheduling (Preemptive) algorithm"""
        n = len(processes)
        completed = 0
        current_time = 0
        results = [None] * n
        gantt_chart = []
        processes_copy = copy.deepcopy(processes)
        last_process = None
        
        while completed != n:
            available = [p for p in processes_copy if p['arrival'] <= current_time and p['remaining'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with highest priority (lowest priority number)
            selected = min(available, key=lambda x: x['priority'])
            
            # If switching process, record in Gantt chart
            if last_process != selected['pid']:
                if last_process is not None and gantt_chart:
                    gantt_chart[-1]['end'] = current_time
                
                gantt_chart.append({
                    'pid': selected['pid'],
                    'start': current_time,
                    'end': current_time + 1
                })
            
            selected['remaining'] -= 1
            
            if selected['remaining'] == 0:
                completion_time = current_time + 1
                turnaround_time = completion_time - selected['arrival']
                waiting_time = turnaround_time - selected['burst']
                
                results[selected['pid'] - 1] = {
                    'pid': selected['pid'],
                    'arrival': selected['arrival'],
                    'burst': selected['burst'],
                    'priority': selected['priority'],
                    'start': selected['arrival'],
                    'completion': completion_time,
                    'turnaround': turnaround_time,
                    'waiting': waiting_time
                }
                completed += 1
            
            last_process = selected['pid']
            current_time += 1
        
        # Close last process segment
        if gantt_chart:
            gantt_chart[-1]['end'] = current_time
        
        return {'results': results, 'gantt': gantt_chart}
    
    def priority_non_preemptive(self, processes):
        """Priority Scheduling (Non-preemptive) algorithm"""
        n = len(processes)
        completed = 0
        current_time = 0
        results = []
        gantt_chart = []
        processes_copy = copy.deepcopy(processes)
        
        while completed != n:
            available = [p for p in processes_copy if p['arrival'] <= current_time and p['remaining'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with highest priority (lowest priority number)
            selected = min(available, key=lambda x: x['priority'])
            
            start_time = current_time
            completion_time = current_time + selected['burst']
            turnaround_time = completion_time - selected['arrival']
            waiting_time = turnaround_time - selected['burst']
            
            results.append({
                'pid': selected['pid'],
                'arrival': selected['arrival'],
                'burst': selected['burst'],
                'priority': selected['priority'],
                'start': start_time,
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
            
            gantt_chart.append({
                'pid': selected['pid'],
                'start': start_time,
                'end': completion_time
            })
            
            selected['remaining'] = 0
            current_time = completion_time
            completed += 1
        
        return {'results': sorted(results, key=lambda x: x['pid']), 'gantt': gantt_chart}
    
    def display_results(self, calculation_results, algorithm):
        """Display calculation results"""
        # Clear previous results
        for widget in self.results_content.winfo_children():
            widget.destroy()
        
        results = calculation_results['results']
        gantt_data = calculation_results['gantt']
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.results_content)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Results Table Tab
        self.create_results_table_tab(notebook, results, algorithm)
        
        # Gantt Chart Tab
        self.create_gantt_chart_tab(notebook, gantt_data)
        
        # Statistics Tab
        self.create_statistics_tab(notebook, results)
    
    def create_results_table_tab(self, notebook, results, algorithm):
        """Create results table tab"""
        table_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(table_frame, text="Results Table")
        
        # Algorithm name
        algo_label = tk.Label(
            table_frame,
            text=f"Algorithm: {algorithm.replace('_', ' ')}",
            font=self.fonts['heading'],
            fg=self.colors['primary'],
            bg=self.colors['white']
        )
        algo_label.pack(pady=(10, 20))
        
        # Create table
        columns = ['PID', 'Arrival', 'Burst', 'Completion', 'Turnaround', 'Waiting']
        if any('priority' in r for r in results if r):
            columns.insert(3, 'Priority')
        
        # Table frame with scrollbar
        table_container = tk.Frame(table_frame, bg=self.colors['white'])
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Headers
        header_frame = tk.Frame(table_container, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X)
        
        for col, header in enumerate(columns):
            label = tk.Label(
                header_frame,
                text=header,
                font=self.fonts['heading'],
                fg=self.colors['white'],
                bg=self.colors['primary'],
                width=12,
                pady=8
            )
            label.grid(row=0, column=col, padx=1, sticky="ew")
        
        # Data rows
        data_frame = tk.Frame(table_container, bg=self.colors['white'])
        data_frame.pack(fill=tk.X)
        
        for i, result in enumerate(results):
            if result is None:
                continue
                
            bg_color = self.colors['light'] if i % 2 == 0 else self.colors['white']
            
            values = [
                result['pid'],
                result['arrival'],
                result['burst']
            ]
            
            if 'priority' in result:
                values.append(result['priority'])
            
            values.extend([
                result['completion'],
                result['turnaround'],
                result['waiting']
            ])
            
            for col, value in enumerate(values):
                label = tk.Label(
                    data_frame,
                    text=str(value),
                    font=self.fonts['body'],
                    bg=bg_color,
                    width=12,
                    pady=5
                )
                label.grid(row=i, column=col, padx=1, sticky="ew")
    
    def create_gantt_chart_tab(self, notebook, gantt_data):
        """Create Gantt chart tab"""
        chart_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(chart_frame, text="Gantt Chart")
        
        # Chart title
        title_label = tk.Label(
            chart_frame,
            text="Gantt Chart",
            font=self.fonts['heading'],
            fg=self.colors['dark'],
            bg=self.colors['white']
        )
        title_label.pack(pady=(10, 20))
        
        # Canvas for Gantt chart
        canvas = tk.Canvas(
            chart_frame,
            width=800,
            height=200,
            bg=self.colors['dark'],
            relief=tk.SUNKEN,
            bd=2
        )
        canvas.pack(padx=20, pady=10)
        
        if not gantt_data:
            canvas.create_text(400, 100, text="No data to display", font=self.fonts['body'])
            return
        
        # Draw Gantt chart
        max_time = max(segment['end'] for segment in gantt_data)
        scale = 700 / max_time if max_time > 0 else 1
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                  '#1abc9c', '#d35400', '#34495e', '#16a085', '#c0392b']
        
        y_position = 50
        x_offset = 50
        height = 40
        
        for segment in gantt_data:
            x1 = x_offset + segment['start'] * scale
            x2 = x_offset + segment['end'] * scale
            
            # Draw process block
            color = colors[(segment['pid'] - 1) % len(colors)]
            canvas.create_rectangle(x1, y_position, x2, y_position + height,
                                  fill=color, outline='white')
            
            # Draw process label
            mid_x = (x1 + x2) / 2
            canvas.create_text(mid_x, y_position + height/2,
                              text=f"P{segment['pid']}", fill='white',
                              font=self.fonts['body'])
            
            # Draw time markers
            canvas.create_line(x1, y_position + height,
                              x1, y_position + height + 10)
            canvas.create_text(x1, y_position + height + 20,
                              text=str(segment['start']),
                              font=self.fonts['small'])
        
        # Draw final time marker
        final_x = x_offset + max_time * scale
        canvas.create_line(final_x, y_position + height,
                          final_x, y_position + height + 10)
        canvas.create_text(final_x, y_position + height + 20,
                          text=str(max_time),
                          font=self.fonts['small'])

    def create_statistics_tab(self, notebook, results):
        """Create statistics tab"""
        stats_frame = tk.Frame(notebook, bg=self.colors['dark'])
        notebook.add(stats_frame, text="Statistics")
        
        # Calculate statistics
        valid_results = [r for r in results if r is not None]
        if not valid_results:
            tk.Label(stats_frame,
                    text="No data available",
                    font=self.fonts['body'],
                    fg=self.colors['white'],
                    bg=self.colors['dark']).pack(pady=20)
            return
        
        avg_turnaround = sum(r['turnaround'] for r in valid_results) / len(valid_results)
        avg_waiting = sum(r['waiting'] for r in valid_results) / len(valid_results)
        throughput = len(valid_results) / max(r['completion'] for r in valid_results)
        
        # Create statistics display with improved styling
        stats_container = tk.Frame(stats_frame, bg=self.colors['dark'])
        stats_container.pack(pady=30)
        
        # Title for statistics
        title_label = tk.Label(
            stats_container,
            text="Process Statistics Summary",
            font=self.fonts['heading'],
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        title_label.pack(pady=(0, 20))
        
        stats = [
            ("Average Turnaround Time:", f"{avg_turnaround:.2f} units"),
            ("Average Waiting Time:", f"{avg_waiting:.2f} units"),
            ("Throughput:", f"{throughput:.2f} processes/unit time"),
            ("Total Processes:", str(len(valid_results))),
            ("Total Time:", f"{max(r['completion'] for r in valid_results)} units")
        ]
        
        for i, (label, value) in enumerate(stats):
            row_frame = tk.Frame(stats_container, bg=self.colors['dark'])
            row_frame.pack(pady=10)
            
            # Label with improved styling
            tk.Label(row_frame,
                    text=label,
                    font=self.fonts['heading'],
                    fg=self.colors['white'],
                    bg=self.colors['dark']).pack(side=tk.LEFT, padx=10)
            
            # Value with different color for better visibility
            tk.Label(row_frame,
                    text=value,
                    font=self.fonts['body'],
                    fg=self.colors['secondary'],
                    bg=self.colors['dark']).pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    app = OSProcessCalculator()