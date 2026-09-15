package work4;

import work4.gui.*; // наші доменні Window, Button, TextField, etc.

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

// Імпортуємо тільки потрібні класи з AWT, без wildcard
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

/**
 * Swing bridge demo: shows a real window + wires Swing events to domain classes.
 * Domain output stays in console (as per stubs), while Swing shows the UI.
 */
public class DemoGuiSwing {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // --- Domain objects (our assignment classes)
            Window dWin = new Window("w1", "MainWindow", "Main Window");
            Button dBtn = new Button("b1", "OkButton");
            TextField dTf = new TextField("t1", "InputField");
            dWin.addChild(dBtn);
            dWin.addChild(dTf);

            LoggerListener loggerAll   = new LoggerListener("L1");
            LoggerListener loggerClick = new LoggerListener("L2", "click");
            ActionHandler action       = new ActionHandler(dTf);

            dBtn.addListener(loggerAll);
            dBtn.addListener(loggerClick);
            dBtn.addListener(action);
            dTf.addListener(loggerAll);
            dWin.addListener(loggerAll);

            // --- Swing UI
            JFrame frame = new JFrame(dWin.getTitle());
            JButton btn = new JButton("OK");
            JTextField tf = new JTextField(20);
            tf.setText(dTf.getText());

            JPanel panel = new JPanel(new GridBagLayout());
            GridBagConstraints c = new GridBagConstraints();
            c.insets = new Insets(8, 8, 8, 8);

            c.gridx = 0; c.gridy = 0;
            panel.add(new JLabel("Input:"), c);

            c.gridx = 1; c.gridy = 0;
            panel.add(tf, c);

            c.gridx = 0; c.gridy = 1; c.gridwidth = 2;
            panel.add(btn, c);

            frame.setContentPane(panel);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            frame.setVisible(true);

            // ---- Reentrancy guards to avoid infinite loops
            final java.util.concurrent.atomic.AtomicBoolean pushingFromSwing   = new java.util.concurrent.atomic.AtomicBoolean(false);
            final java.util.concurrent.atomic.AtomicBoolean updatingFromDomain = new java.util.concurrent.atomic.AtomicBoolean(false);

            // Swing -> Domain
            DocumentListener dl = new DocumentListener() {
                private void push() {
                    if (updatingFromDomain.get()) return; // ignore programmatic updates
                    String newText = tf.getText();
                    // update domain only if changed (should be always for user edits)
                    if (!newText.equals(dTf.getText())) {
                        try {
                            pushingFromSwing.set(true);
                            dTf.setText(newText);
                        } finally {
                            pushingFromSwing.set(false);
                        }
                    }
                }
                public void insertUpdate(DocumentEvent e) { push(); }
                public void removeUpdate(DocumentEvent e) { push(); }
                public void changedUpdate(DocumentEvent e) { push(); }
            };
            tf.getDocument().addDocumentListener(dl);

            // Domain -> Swing (reflect ActionHandler changes)
            dTf.addListener((eventType, source) -> {
                if ("textChanged".equals(eventType) && source instanceof TextField) {
                    if (pushingFromSwing.get()) return; // this change came from Swing already
                    String domainText = ((TextField) source).getText();
                    // update Swing only if actually different
                    if (!domainText.equals(tf.getText())) {
                        try {
                            updatingFromDomain.set(true);
                            SwingUtilities.invokeLater(() -> {
                                tf.setText(domainText);
                                // caret to end for nicer UX (optional):
                                tf.setCaretPosition(tf.getText().length());
                            });
                        } finally {
                            // small defer to let EDT apply text before we allow DL again
                            SwingUtilities.invokeLater(() -> updatingFromDomain.set(false));
                        }
                    }
                }
            });

            // Button click bridges
            btn.addActionListener(e -> dBtn.click());

            frame.addWindowListener(new WindowAdapter() {
                @Override public void windowClosed(WindowEvent e) { dWin.close(); }
            });
        });
    }
}