
   function cambiar(list){
    aa=(list==0)?"list2":"list1";
    bb=(list==0)?"list1":"list2";
    a=document.forms[0][aa];
    b=document.forms[0][bb];
    if(a.value==''){return false;}
    seVa=a.options[a.selectedIndex];
    a[a.selectedIndex]=null;
    b.options[b.options.length]=seVa;
    }