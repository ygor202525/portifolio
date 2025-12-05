package calculo_salarios;

import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.DecimalFormat;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.border.EmptyBorder;

public class Salarios extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField txtSalario;
	private JTextField txtPercentual;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Salarios frame = new Salarios();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Salarios() {
		
		
		    setTitle("Janela de Teste");
		    setSize(400, 300);
		    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		    setLocationRelativeTo(null); // Centraliza na tela
		
		
		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 494, 418);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Empresa salários");
		lblNewLabel.setFont(new Font("Arial Black", Font.PLAIN, 22));
		lblNewLabel.setBounds(10, 0, 223, 38);
		contentPane.add(lblNewLabel);
		
		JLabel lblNewLabel_1 = new JLabel("Simulação de hipotética folha de pagamento");
		lblNewLabel_1.setForeground(new Color(0, 0, 255));
		lblNewLabel_1.setFont(new Font("Arial", Font.ITALIC, 14));
		lblNewLabel_1.setBounds(10, 28, 300, 38);
		contentPane.add(lblNewLabel_1);
		
		JLabel lblNewLabel_2 = new JLabel("Salário");
		lblNewLabel_2.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblNewLabel_2.setBounds(10, 77, 101, 21);
		contentPane.add(lblNewLabel_2);
		
		JLabel lblNewLabel_2_1 = new JLabel("Percentual de desconto");
		lblNewLabel_2_1.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblNewLabel_2_1.setBounds(10, 145, 233, 21);
		contentPane.add(lblNewLabel_2_1);
		
		JLabel lblNewLabel_2_1_1 = new JLabel("RESULTADOS");
		lblNewLabel_2_1_1.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_2_1_1.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblNewLabel_2_1_1.setBounds(86, 222, 233, 21);
		contentPane.add(lblNewLabel_2_1_1);
		
		JLabel lblLiquido = new JLabel("");
		lblLiquido.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblLiquido.setBounds(10, 254, 446, 21);
		contentPane.add(lblLiquido);
		
		JLabel lblAnual = new JLabel("");
		lblAnual.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblAnual.setBounds(10, 286, 233, 21);
		contentPane.add(lblAnual);
		
		JLabel lblDecimo = new JLabel("");
		lblDecimo.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblDecimo.setBounds(10, 317, 366, 21);
		contentPane.add(lblDecimo);
		
		JLabel lblFerias = new JLabel("");
		lblFerias.setFont(new Font("Arial Black", Font.PLAIN, 14));
		lblFerias.setBounds(10, 349, 233, 21);
		contentPane.add(lblFerias);
		
		txtSalario = new JTextField();
		txtSalario.setFont(new Font("Arial", Font.PLAIN, 14));
		txtSalario.setBounds(10, 98, 162, 23);
		contentPane.add(txtSalario);
		txtSalario.setColumns(10);
		
		txtPercentual = new JTextField();
		txtPercentual.setFont(new Font("Arial", Font.PLAIN, 14));
		txtPercentual.setColumns(10);
		txtPercentual.setBounds(10, 169, 78, 23);
		contentPane.add(txtPercentual);
		
		JButton btnCalcular = new JButton("Calcular");
		btnCalcular.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
				double salario  = Double.parseDouble(txtSalario.getText());
				double percentual = Double.parseDouble(txtPercentual.getText());
				
				
				double resultado = salario-(salario/100)*percentual;
				double anual = resultado*12;
				double decimoTerceiro = resultado;
				double ferias = resultado+(resultado/3);
			
				
	//formatação dos resultados(calculos) , apenas duas casas pós virgula
				DecimalFormat formato = new DecimalFormat ("#0.00");
				String resultadoFormatado = formato.format(resultado);
				String anualFormatado = formato.format(anual);
				String decimoTerceiroFormatado = formato.format(decimoTerceiro);
				String feriasFormatado = formato.format(ferias);
				
				
				lblLiquido.setText("Valor Mensal: R$ "+resultadoFormatado);
				lblAnual.setText ("Valor anual: R$ "+anualFormatado);
				lblDecimo.setText("Valor do décimo terceiro: R$: "+decimoTerceiroFormatado);
				lblFerias.setText("Valor de férias: R$: "+feriasFormatado);
				
				
				
				
			}
		});
		btnCalcular.setFont(new Font("Arial Black", Font.BOLD, 14));
		btnCalcular.setBounds(150, 196, 109, 23);
		contentPane.add(btnCalcular);
	}
}
