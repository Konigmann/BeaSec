<%@ Page
    Title="HyperCat"
    Language="C#"
    MasterPageFile="~/Plain.Master" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <style type="text/css">
        body {
            font-family: sans-serif;
            margin: auto;
        }

        .radio-group {
            font-family: monospace;
        }

        textarea {
            width: 100%;
            font-family: monospace;
        }

        #key {
            font-family: monospace;
        }

        #result {
            font-size: 18px;
        }
    </style>
</asp:Content>

<asp:Content ID="Content2" ContentPlaceHolderID="main" runat="Server">

    <h2>Nested Object Lookup</h2>
    <p>This file is also hosted at:  http://hypercat.info/_test/NestedResult.aspx</p>


    <div class="radio-group">
        <label>
            <input type="radio" name="example" onclick="setExample(1)" checked="checked" />
            {"a":{"b":{"c":"d"}}} — a/b/c</label><br />
        <label>
            <input type="radio" name="example" onclick="setExample(2)" />
            {"x":{"y":{"z":"w"}}} — x/y/z</label><br />
        <label>
            <input type="radio" name="example" onclick="setExample(3)" />
            {"p":{"q":{"r":"s"}}} — p/q/r</label><br />
        <label>
            <input type="radio" name="example" onclick="setExample(4)" />
            {"h":{"s":{"a":"$"}}} — h/s/a</label><br />
    </div>

    <br />

    <label for="nestedObject">Nested Object:</label><br />
    <textarea id="nestedObject" rows="3" cols="100" style="width: 100%; font-family: monospace;">{ "a": { "b": { "c": "d" } } }</textarea>
    <br />

    <label for="key">Key (a/b/c, x/y/z):</label><br />
    <input type="text" id="key" name="key" value="a/b/c" /><br />
    <br />

    <button type="button" onclick="returnValue()">Return the Value</button>

    <h3>Result:</h3>
    <xmp id="result"></xmp>

    <script type="text/javascript">
        function getValueByPath( obj, path )
        {
            var keys = path.split( '/' );
            var current = obj;
            for( var iii = 0; iii < keys.length; iii++ )
            {
                var key = keys[iii];
                if( current && typeof current === 'object' && key in current )
                {
                    current = current[key];
                } else
                {
                    return undefined;
                }
            }
            return current;
        }

        function returnValue()
        {
            var nestedObject = document.getElementById( "nestedObject" ).value;
            var key = document.getElementById( "key" ).value;
            var resultArea = document.getElementById( "result" );

            try
            {
                var jsonObj = JSON.parse( nestedObject );
                var value = getValueByPath( jsonObj, key );
                resultArea.textContent = value !== undefined
                    ? "The value is: " + JSON.stringify( value )
                    : "Not found.";
            } catch( e )
            {
                resultArea.textContent = "Error: " + e.message;
            }
        }


        function setExample( nnn )
        {
            var textarea = document.getElementById( "nestedObject" );
            var keyInput = document.getElementById( "key" );

            if( nnn === 1 )
            {
                nestedObject.value = '{ "a": { "b": { "c": "d" } } }';
                key.value = 'a/b/c';
            } else if( nnn === 2 )
            {
                nestedObject.value = '{ "x": { "y": { "z": "w" } } }';
                key.value = 'x/y/z';
            } else if( nnn === 3 )
            {
                nestedObject.value = '{ "p": { "q": { "r": "s" } } }';
                key.value = 'p/q/r';
            } else if( nnn === 4 )
            {
                nestedObject.value = '{ "h": { "s": { "a": "$" } } }';
                key.value = 'h/s/a';
            }
            var resultArea = document.getElementById( "result" );
            resultArea.textContent = "";
        }
    </script>
</asp:Content>
