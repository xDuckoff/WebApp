function get_tree(objectId) {
    $.ajax({
        url: "/tree",
        type: "GET",
        data: {
            chat: chat_index
        },
        dataType: "json",
        success: function( nodeStructure ) {
            var config = {
                    container: "#" + objectId,
                    levelSeparation: 70,
                    siblingSeparation: 70,
                    rootOrientation: "WEST",
                    connectors: {
                        style:{
                            stroke: 'white'
                        }
                    }
                };

            var simple_chart_config = {
                    chart: config,
                    nodeStructure: nodeStructure
                };
            var tree = new Treant(simple_chart_config, function(){}, $);
            draw_node(chosen_commit);
        }
    });
}

function draw_node(commitIndex){
    var nodes = $('.commit_node');
    nodes.removeClass('chosen')
            .filter('[data-id=' + commitIndex + ']')
            .addClass('chosen');
}

jQuery(function($) {
    get_tree('tree');
    $('#tree').on("click", ".commit_node", function(){
        var commitId = $(this).data('id');
        draw_node(commitId);
        get_code(commitId);
    });
});