/**
 * @namespace
 */
var SOClone =
{
    /**
     * Finds any <pre><code></code></pre> tags which aren't registered for
     * pretty printing, adds the appropriate class name and invokes prettify.
     */
    styleCode: function()
    {
        var style = false;

        $("pre code").parent().each(function()
        {
            if (!$(this).hasClass('prettyprint'))
            {
                $(this).addClass('prettyprint');
                style = true;
            }
        });

        if (style)
        {
            prettyPrint();
        }
    }
};
