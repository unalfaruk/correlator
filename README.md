# **Correlator: The Signal Correlation Visualizer**

Welcome to **Correlator**, your go-to tool for understanding signal correlation in a visual and step-by-step manner. With Correlator, you can watch how signals interact with each other as they shift step-by-step and see the correlation process unfold in real-time!

## **Features**

- **Step-by-Step Visualization:** Click "Steps" to shift one signal over another incrementally and view the resulting correlation at each step.
- **Animation Mode:** Click "Run Animation" to automatically progress through all the steps and visualize the entire correlation process in one go.
- **Result Reporting:** Once the correlation is complete, the final result is printed out for your review.
- **Logging:** A log file with the current date and time is generated in the script's directory, capturing the details of the correlation process.

## **Installation**

To get started with Correlator, you need to have Python installed on your machine. Correlator uses the `matplotlib` library for plotting, which you can install via pip if you haven't already:

```bash
pip install matplotlib
```

Clone the repository or download the script directly:

```bash
git clone https://github.com/yourusername/correlator.git
```

Navigate to the directory containing the script:

```bash
cd correlator
```

## **Usage**

1. **Run the Tool:**
   Execute the script using Python. This will open a graphical user interface (GUI) where you can interact with the tool.

   ```bash
   python correlator.py
   ```

2. **Interact with the GUI:**
   - **Steps Button:** Click this to shift one of the signals over the other incrementally. This will generate plots showing the signals and their correlation at each step.
   - **Run Animation Button:** Click this to automatically progress through all the steps. The tool will animate the shifting of the signals and update the plots until the correlation is complete.

3. **View Results:**
   - After completing the steps or animation, the final correlation result will be printed in the console.
   - A log file will be generated in the script's directory with the current date and time, capturing details about the correlation process.

## **Example**

Put your signals into *signal1* and *signal2* variable as array.

1. Launch the tool:

   ```bash
   python correlator.py
   ```

2. Click the "Steps" button to observe the correlation process step-by-step.

3. Alternatively, click "Run Animation" to see the correlation progress automatically.

4. Check the console for the final correlation result and look for a log file in the directory for a detailed record of the process.

## **Contributing**

As an amateur project, contributions are welcome! Feel free to open issues or submit pull requests with improvements or new features. Please ensure to document your changes and test thoroughly.

## **Contact**

If you have any questions or need support, you can reach out to me.

