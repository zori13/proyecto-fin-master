from web3 import Web3
from ZoriProPrestamoDefi import ZoriProPrestamoDefi
from Web3.middleware import geth_poa_middelware
from eth_account import Account

ganache_url="http://127.0.0.1:7545"
w3=Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("No se pudo conectar a la red Etherum")
    exit()
else:
    print("Conexión realizada")

contract_address = "0xFDcBe80A21416D78b6dc4C01090bBdfe0bC3aEC6"
abi="[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"clientes","outputs":[{"internalType":"bool","name":"activado","type":"bool"},{"internalType":"uint256","name":"saldoGarantia","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"empleadosPrestamista","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetalleDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct ZoriProPrestamoDefi.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]"
contract = w3.eth.contract(address=contract_address, abi=abi)

def alta_prestamista(nuevo_prestamista_address): #solo puede añadir un nuevo prestamista el socio principal, se le pasa como parámetro el address del nuevo prestamista
   account = w3.eth.account.privateKeyToAccount(0x8ea8ab46ae6934be25eff95fde59abec622352f05f6aee7a09f794e3e1d4b61f) #se añade la clave privada del socio principal
   w3.middleware_onion.inject(geth_poa_middelware, layer = 0) #para manejar las transacciones con ganache
   w3.eth.default_account = account.address  
      
   #se construye la transacción
   tx = contract.functions.cambiarPrestamista(nuevo_prestamista_addres).build_transaction({
       'from': w3.eth.default_account,
       'gas': 3000000,
       'gasPrice': w3.toWei('50', 'gwei'),
   })
   
   #firmar la transacción
   tx_firmada = w3.eth.account.signTransaction(tx, private_key=account_privateKey)
   
   #enviar tx a ganache
   tx_hash = w3.eth.send_raw_transaction(tx_firmada.rawTransaction)
   
   #esperar confirmación
   w3.eth.wait_for_transaction_receipt(tx_hash)
   return tx_hash

#Llamada a la función
nuevo_prestamista_address = contract.functions.nuevo_prestamista_address().call()
restultado = alta_prestamista(nuevo_prestamista_address)
print(f'Transaccion enviada: {resultado}')

def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    cliente_registrado = contract.functions.verificar_cliente(nuevo_cliente_address).call()
    if not cliente_registrado:
        tx = contract.functions.registrar_cliente(nuevo_cliente_address).buildTransaction({
            'from': prestamista_address,
            'nonce':  web3.eth.getTransactionCount(prestamista_address),
            'gas': 20000000,
            'gasPrice': web3.toWei('50', 'gwei')
            })
        
        tx_firmada = web3.eth.account.signTransaction(transaccion, private_key=prestamista_private_key)
        tx_hash = web3.eth.sendRawTransaction(transaccion_firmada.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt.status == 1:
            return "Cliente registrado con exito"
        else:
            return "Error: La transaccion ha fallado"
    else:
        return "El cliente ya esta registrado"

nuevo_cliente_address = contract.functions.nuevo_cliente_address().call()
prestamista_address = contract.functions.prestamista_address().call()
prestamista_private_key = contract.functions.prestamista_private_key().call()
restultado = alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key)
print(restultado)

def depositar_garantia (direccion_cliente, valor, clave_privada_cliente):
    nonce = w3.eth.get_transaction_count(direccion_cliente)
    tx = contract.functions.depositar_garantia().build_transaction({
        'from': direccion_cliente,
        'value': valor,
        'nonce': nonce,
    })
    
    tx_firmada = w3.eth.account.sign_transaction(tx, clave_privada_cliente)
    tx_hash = w3.eth.send_raw_transaction(tx_firmada.raw_transaction) 
    recibido =w3.eth.waitForTransactionReceipt(tx_hash)
    if recibido.status == 1:
        return "Garantia depositada con exito"
    else:
        return "Fallo en la transaccion"
    
direccion_cliente = "contract.functions.direccion_cliente().call()"
valor="contract.functions.monto().call()"
clave_privada_cliente = "contract.functions.clave_privada_cliente().call()"

resultado = depositar_garantia(direccion_cliente, valor, clave_privada_cliente)
print(resultado)

def solicitar_prestamo (direccion_cliete, monto, plazo, clave_privada_cliente):
    def verificar_garantia(direccion_cliente):
        VER COMO ENLAZAR ESTO CON EL CONTRATO INTELIGENTE
        return true
    
    def enviar_solicitud_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
         VER COMO ENLAZAR ESTO CON EL CONTRATO INTELIGENTE
         RESPUESTA EXITOSA CON ID DE PRESTAMO
         return "id_prestamo"
        
    if verificar_garantia(direccion_cliente):
        id_prestamo = enviar_solicitud_prestamo(direccion_cliente, monto, plazo,clave_privada_cliente)
        if id_prestamo:
            return "Transaccion fallida"
        else:
            return "Error al solicitar el prestamo"
    else:
        return "No hay suficiente garantia"

    
