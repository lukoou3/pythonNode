var map = new BMap.Map("allmap");
map.centerAndZoom(new BMap.Point(116.403765, 39.914850), 5);
map.enableScrollWheelZoom();


var boundaries = [];
var pointArray = [];
$("#query").on('click', function(){
    boundaries = [];
    $(this).prop("disabled",true);
    queryButtonEnabled(this);
    getBoundary($.trim($("#keyword").val()));
});
$("#download").on('click', function(){
    if(boundaries && boundaries.length)
    {
        $(this).prop("disabled",true);
        queryButtonEnabled(this);
        $.post("/download",getPointRange(getCoordinateRange(boundaries)));
    }
});

async function queryButtonEnabled(dom,time=3) {
    await sleep(time);
    $(dom).prop("disabled",false);
}

function sleep(second) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, second*1000);
    })
}

function getBoundary(city){
    var bdary = new BMap.Boundary();
    bdary.get(city, function(rs){       //获取行政区域
        boundaries = rs.boundaries;
        map.clearOverlays();        //清除地图覆盖物
        var count = boundaries.length; //行政区域的点有多少个
        if (count === 0) {
            alert('未能获取当前输入行政区域');
            return ;
        }

        pointArray = [];
        for (var i = 0; i < count; i++) {
            var ply = new BMap.Polygon(boundaries[i], {strokeWeight: 2, strokeColor: "#ff0000"}); //建立多边形覆盖物
            map.addOverlay(ply);  //添加覆盖物
            pointArray = pointArray.concat(ply.getPath());
        }
        map.setViewport(pointArray);    //调整视野
    });
}

function getPointRange(obj){
    var projection =new BMap.MercatorProjection();
    var point1 = projection.lngLatToPoint(new BMap.Point(obj.minX, obj.minY));
    var point2 = projection.lngLatToPoint(new BMap.Point(obj.maxX, obj.maxY));
    return {minX:point1.x,minY:point1.y,maxX:point2.x,maxY:point2.y};
}

function getCoordinateRange(boundaries,obj){
    var obj = {};
    var minX = 0,maxX = 0,minY = 0,maxY = 0,array;

    var ply = new BMap.Polygon(pointArray , {strokeWeight: 2, strokeColor: "#ff0000"}); //建立多边形覆盖物
    var bounds = ply.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    minX = sw.lng;
    maxX = ne.lng;
    minY = sw.lat;
    maxY = ne.lat;

    /*for(var j=0;j<pointArray.length;j++)
    {
        var org =   pointArray[j];
        if(minX == 0)
        {
            minX = org.lng;
            maxX = org.lng;
            minY = org.lat;
            maxY = org.lat;
        }
        else
        {
            if(org.lng < minX)
            {
                minX = org.lng;
            }
            else if(org.lng > maxX)
            {
                maxX = org.lng;
            }

            if(org.lat < minY)
            {
                minY = org.lat;
            }
            else if(org.lat > maxY)
            {
                maxY = org.lat;
            }
        }
    }*/

    /*for(var i=0;i<boundaries.length;i++)
    {
        array = boundaries[i].split(";");

        for(var j=0;j<array.length;j++)
        {
            var array1 =   array[j].split(",")
            var org = {lng:array1[0]*1,lat:array1[1]*1};
            if(minX == 0)
            {
                minX = org.lng;
                maxX = org.lng;
                minY = org.lat;
                maxY = org.lat;
            }
            else
            {
                if(org.lng < minX)
                {
                    minX = org.lng;
                }
                else if(org.lng > maxX)
                {
                    maxX = org.lng;
                }

                if(org.lat < minY)
                {
                    minY = org.lat;
                }
                else if(org.lat > maxY)
                {
                    maxY = org.lat;
                }
            }
        }
    }*/

    obj.minX=minX;
    obj.maxX=maxX;
    obj.minY=minY;
    obj.maxY=maxY;
    return obj;
}