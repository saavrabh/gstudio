CKEDITOR.plugins.add('addAudio',
{
    init: function(editor)
    {
        //plugin code goes here
        var pluginName = 'addAudio';
        var groupId = editor.config.groupID.group_id;
        var nodeId = editor.config.nodeID.node_id;
        var url = "/" + groupId + "/audio";
        // var textAreaId = "textarea-"+nodeId;
        var textAreaId = editor.config.textarea_id;
        CKEDITOR.dialog.add(pluginName, this.path + 'plugin.js');
        editor.addCommand(pluginName, new CKEDITOR.dialogCommand(pluginName));

        editor.addCommand("addAudio", {
            exec: function() {

                    $.ajax({
                        type: "GET",
                        url: url,
                        datatype: "html",
                        data:{

                        },
                        success: function(data) {
                          $("#group_imgs_on_modal").html(data);
                          $('#group_imgs_on_modal').foundation('reveal', 'open');
                        }
                    });
            }
        });

        editor.ui.addButton('addAudio',
            {
                label: 'Record Audio or add audio file  from this Group',
                command: pluginName,
                icon: this.path + 'images/fi-music.svg'
            });

    }
});
