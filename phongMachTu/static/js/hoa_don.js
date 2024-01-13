function pay(id) {
    fetch(`/api/staff/thanh-toan-hoa-don/${id}`, {
        method: "put"
    }).then(function(res){
        return res.json();
    }).then(function(data){
    if (data.status === 200)
        location.reload();
    else
        alert(data.err_msg)
    })
}
