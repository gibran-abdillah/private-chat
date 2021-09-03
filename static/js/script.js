$(document).ready(function() {
    const this_domain = location.protocol + '//' + document.domain + ':' + location.port;
    const socket = io.connect(this_domain);
    const private_socket = io.connect(this_domain + '/private');
    console.log(this_domain + '/private')

    var username = $('#my_username').val();

    socket.on('connect', function(){
        console.log('connected')
    })

    private_socket.on('connect', function(){
        console.log('Private Socket Connected')
    })

    $('#first_submit').on('click', function(){
        username = $('#my_username').val();
        socket.emit('username', $('#my_username').val())
    })
    socket.on('error_username', function(){
        $('#error').html('username has been added before')
    })
    socket.on('valid_username', function(response){
        console.log('valid')
        $('#first_step').hide();
        document.getElementById('second_step').style.display = 'block';
    })

    $('#cari').on('click', function(){
        private_socket.emit('find_partner', username);
        $('#second_step').append('<p>In Queue</p>')
    })
    private_socket.on('found_partner', function() {
        console.log('Found Partner');
        $('#second_step').append('<p>Partner Founded</p>')
    })


})