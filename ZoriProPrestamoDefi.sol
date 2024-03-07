// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; 

contract ZoriProPrestamoDefi{
    address public socioPrincipal;
    struct Prestamo{
        uint256 id; //identificador del prestamo
        address prestatario; //cliente
        uint256 monto; //cantidad adeudada
        uint256 plazo; //duracion del tiempo tras ser aceptado el prestamo en seg
        uint256 tiempoSolicitud; // desde que se solicita el prestamo hasta que se aprueba
        uint256 tiempoLimite; // desde que se aprueba hasta que finaliza el plazo
        bool aprobado; // cuando se acepte el prestamo se pondra a true
        bool reembolsado; // cuando se devuelva el monto adeudado se pondrá a true
        bool liquidado; // si no se reembolsa el prestamo se pone a true y el prestamista se queda con la garantia
   }

    struct Cliente{
        bool activado; // indica si el cliente está activo y resgistrado
        uint256 saldoGarantia; // saldo total de garantias depositadas de todos los prestamos que hubiese
        mapping(uint256=>Prestamo) prestamos;//mapeo ID del prestamo al struct Prestamo
        uint256[] prestamoIds; //array que lista la ID de los prestamos asociados a un cliente
    }

    mapping(address=>Cliente) public clientes; //mapea las direcciones de clientes al struct Cliente
    mapping(address=>bool)public empleadosPrestamista;//mapea direcciones a un bool que indica si el addres es prestamsita
     
    event SolicitudPrestamo(
        address indexed prestatario,
        uint256 monto,// se le pasan estos datos al finalizar la solicitud del prestamo
        uint256 plazo
    );
    event PrestamoAprobado(
        address indexed prestatario,
        uint256 monto//se pasan estos datos cuando es aprobado el prestamo
        );
    event PrestamoReembolsado(
        address indexed prestatario,
        uint256 monto//se le pasan estos datos cuando el prestamo es reembolsado
    );
    event GarantiaLiquidada(
        address indexed prestatario,
        uint256 monto//se le pasan estos datos cuando la garantia es liquidada
    );

    modifier soloSocioPrincipal(){
        require(socioPrincipal==msg.sender, "Solo puede acceder el socio principal");
        _;
    }
    modifier soloEmpleadoPrestamista(){
        require(empleadosPrestamista[msg.sender]==true, "No puedes conceder prestamos");
        _;
    }
    modifier soloClienteRegistrado(){
        require(clientes[msg.sender].activado==true, "Cliente no registrado o no activado");
        _;
    }

    constructor(){
        socioPrincipal==msg.sender;
        empleadosPrestamista[socioPrincipal]=true;
    }
    //funcion que da de alta al nuevo prestamista, np porque modifica el mapping empleadosPrestamista
    //si ya esta dado de alta se le envia un error.
    function altaPrestamista(address nuevoPrestamista)public soloSocioPrincipal {
        require(empleadosPrestamista[nuevoPrestamista]=false, "Ya has sido dado de alta");
        empleadosPrestamista[nuevoPrestamista]=true;

    }

    function altaCliente(address nuevoCliente) public soloEmpleadoPrestamista {
        require(!clientes[nuevoCliente].activado,"Ya estas registrado");
        Cliente storage structNuevoCliente = clientes[nuevoCliente];
        structNuevoCliente.saldoGarantia = 0;
        structNuevoCliente.activado = true;
    }

    function depositarGarantia() public payable soloClienteRegistrado{
        require(msg.value>0,"Debe enviar una cantidad mayor que 0");
        Cliente storage cliente = clientes[msg.sender];
        cliente.saldoGarantia += msg.value;
    }

    function solicitarPrestamos(uint256 monto_, uint256 plazo_) public soloClienteRegistrado returns (uint256){
        require(clientes[msg.sender].saldoGarantia>=monto_, "El deposito de la garantia es inferior al monto que se solicita");
        uint256 nuevoId = clientes[msg.sender].prestamoIds.length +1;
        Prestamo storage nuevoPrestamo = clientes[msg.sender].prestamos[nuevoId];
        nuevoPrestamo.id=nuevoId;
        nuevoPrestamo.prestatario=msg.sender;
        nuevoPrestamo.monto = monto_;
        nuevoPrestamo.plazo = plazo_;
        nuevoPrestamo.tiempoSolicitud = block.timestamp;
        nuevoPrestamo.tiempoLimite = 0;
        nuevoPrestamo.aprobado = false;
        nuevoPrestamo.reembolsado = false;
        nuevoPrestamo.liquidado = false;
        clientes[msg.sender].prestamoIds.push(nuevoId);
        emit SolicitudPrestamo(nuevoPrestamo.prestatario, nuevoPrestamo.monto, nuevoPrestamo.plazo);
        return nuevoId;
    }

    function aprobarPrestamo(address prestatario_, uint256 id_) public soloEmpleadoPrestamista {
        Cliente storage prestatario = clientes[prestatario_];
        require(id_ > 0, "No estas registrado como prestatario");
        require(prestatario.prestamoIds.length>=id_, "El id del prestamo no es valido");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(!prestamo.aprobado,"Tu prestamo no esta aprobado");
        require(!prestamo.reembolsado,"Tu prestamo se ha reembolsado");
        require(!prestamo.liquidado,"Tu prestamo se ha liquidado ");
        prestamo.aprobado=true;
        prestamo.plazo= block.timestamp + prestamo.plazo;
        emit PrestamoAprobado(prestatario_, prestamo.monto);
    }

    function reembolsarPrestamo(uint256 id_) public soloClienteRegistrado{
        Cliente storage prestatario = clientes[msg.sender];
        require(id_> 0, "El identificador no es valido");
        require(prestatario.prestamoIds.length>=id_, "El identificador del prestamo no es valido");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(prestamo.prestatario== msg.sender, "No puedes acceder al reembolso ");
        require(prestamo.aprobado,"Tu prestamo no esta aprobado");
        require(!prestamo.reembolsado,"Tu prestamo se ha reembolsado");
        require(!prestamo.liquidado,"Tu prestamo se ha liquidado ");
        require(prestamo.tiempoLimite>=block.timestamp,"El tiempo de vida de tu prestamo se ha excedido");
        payable(socioPrincipal).transfer(prestamo.monto);
        prestamo.reembolsado = true;
        prestatario.saldoGarantia -= prestamo.monto;
        emit PrestamoReembolsado(prestamo.prestatario, prestamo.monto);
    }

    function liquidarGarantia (address prestatario_, uint256 id_) public soloEmpleadoPrestamista{
        Cliente storage prestatario = clientes[prestatario_];
        require(id_> 0, "El identificador no es valido");
        require(prestatario.prestamoIds.length>=id_, "El identificador del prestamo no es valido");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(prestamo.aprobado, "El prestamo no ha sido aprobado");
        require(!prestamo.reembolsado, "El prestamo ya ha sido reembolsado");
        require(!prestamo.liquidado, "El prestamo ha sido liquidado");
        require(prestamo.tiempoLimite>=block.timestamp,"El tiempo de vida de tu prestamo se ha excedido");
        payable(socioPrincipal).transfer(prestamo.monto);
        prestamo.liquidado = true;
        prestatario.saldoGarantia -= prestamo.monto;
        emit GarantiaLiquidada(prestamo.prestatario, prestamo.monto);   
    }

    function obtenerPrestamosPorPrestatario(address prestatario_) public view returns(uint256[] memory){
        return (clientes[prestatario_].prestamoIds);
    }

    function obtenerDetalleDePrestamo(address prestatario_, uint256 id_) public view returns(Prestamo memory) {
        return (clientes[prestatario_].prestamos[id_]);
    }

    
}