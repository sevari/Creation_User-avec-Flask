from flask import Flask, render_template,request,jsonify
import paramiko

app = Flask(__name__)

# eto no manao appel ny acceuil izay misy ny input rehetra
@app.route('/')
def index():
    return render_template('acceuil.html')

# eto no manao recuperation anle formulaire
@app.route('/create_user', methods=['POST'])
def create_user():
    new_username = request.form['username']
    new_password = request.form['password']
    try:
        # manao connection ssh @alalan'ny utilisateur existant
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ity ny information mahakasika ny utilisateur existant izay manana droit afaka micreer utilisateur
        ssh.connect('192.168.134.105', username='slash', password='010203')
        # ity no commande ahafahana manao creation utilisateur miaraka @ilay mot de passe interactive
        create_user_command = f'echo "010203" | sudo -S adduser {new_username}'
    
        stdin, stdout, stderr = ssh.exec_command(create_user_command)

        exit_status = stdout.channel.recv_exit_status()
  

        if exit_status == 0:

            set_password_command = f'echo "{new_password}" | sudo -S passwd {new_username}'
            stdin, stdout, stderr = ssh.exec_command(set_password_command)
            ssh.close()

            return jsonify({'success': True, 'message': 'Utilisateur cree avec succes'})
        else:
            error_message = stderr.read().decode('utf-8').strip()
            ssh.close()
            return jsonify({'success': False, 'message': f'Erreur lors de la creation : {error_message}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Une erreur est survenue : {str(e)}'})
if __name__ == '__main__':
    app.run(debug=True)     
