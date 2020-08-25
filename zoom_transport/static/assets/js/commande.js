 $(document).ready(function()
{
   

  $(document).on('click','.openModal', function () {
      $('.number').text($(this).data('id'));
     
      var cmdId = $(this).data('id');
      $('#btn-assign').attr('data-cmd',$(this).data('id'));
      $('#assignTo').modal('show');

  });
  $(document).on('click','#btn-assign', function () {

        var cmd_id = $(this).attr('data-cmd');
        $.ajax({
            url: $(this).attr('data-action'),
            data: {'id':cmd_id},
            dataType: 'json',
            success: function (data) {
                if(data.statut == "success"){
                    toastr.success(data.message);
                    $('#assignTo'+cmd_id).modal('hide');
                    location.reload();
                }
            }
        });



  });

 });