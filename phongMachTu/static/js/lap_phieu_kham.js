var i = localStorage.getItem('i') || 1;

function addThuoc(ten) {
    fetch("/api/lap-phieu-kham", {
        method: "post",
        body :JSON.stringify({
            "id": i,
            "ten": ten,
        }),
        headers:{
        'Content-Type' : 'application/json'
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.info(data)
        i++;
        localStorage.setItem('i', i);
        location.reload();
    })
}

function deleteThuoc(id, obj){
    if (confirm("Bạn chắc chắn xóa?") === true){
        obj.disable = true;
        fetch(`/api/lap-phieu-kham/${id}`, {
            method: "delete",
        }).then(function(res){//Thuc thi theo kieu bat dong bo, res la du lieu tra ve tu ham addToCart
            return res.json()
        }).then(function(data){// data la res.json()
            obj.disable = false;
            let t = document.getElementById(`thuoc${id}`);
            t.style.display = "none";
        })
    }
}