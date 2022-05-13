#
#-*-coding:utf8;-*-
"""
This is a sample project which use SL4A UI Framework,
There is another Sample project: https://github.com/qpython-android/qpy-calcount

#中国条码查询中心
#https://www.gds.org.cn/#/barcodeList/index?type=barcode&keyword=6901108291090 

"""
import qpy
import androidhelper
import urllib.request as ur
from qsl4ahelper.fullscreenwrapper2 import *

droid = androidhelper.Android()

class MainScreen(Layout):
    def __init__(self):
        self.scanbarcode_result_list=[]
        super(MainScreen,self).__init__(str("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#ff0E4200"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<ImageView
		android:id="@+id/logo"
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:layout_weight="10"
	/>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="vertical"
		android:layout_weight="20">

		<TextView
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:textSize="8dp"
			android:text="扫码结果"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"
		/>
    </LinearLayout>

	<ListView
		android:id="@+id/data_list"
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:layout_weight="55"
		android:gravity="center"
 />

	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="horizontal"
		android:layout_weight="8">
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="扫码"
			android:id="@+id/but_scanbarcode"
			android:textSize="8dp"
			android:background="#ffEFC802"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
			<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="复制"
			android:id="@+id/but_copybarcode"
			android:textSize="8dp"
			android:background="#00BFFF"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="取消"
			android:id="@+id/but_exit"
			android:textSize="8dp"
			android:background="#ff06AF00"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
	</LinearLayout>
</LinearLayout>
"""),"SL4AApp")

    def ButtonText(self,button):
        droid = FullScreenWrapper2App.get_android_instance()
        Lc=len(button)
        if Lc>2:droid.dialogSetNeutralButtonText(button[2])
        if Lc>1:droid.dialogSetNegativeButtonText(button[1])
        if Lc==0:button=('OK',)
        droid.dialogSetPositiveButtonText(button[0])
    OK=('OK',)
    def Button(self,title='Test',message='Click OK',button=OK):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.dialogCreateAlert(title, message)
        self.ButtonText(button)
        droid.dialogShow()
        return droid.dialogGetResponse().result

    def on_show(self):
        self.views.but_exit.add_event(click_EventHandler(self.views.but_exit, self.exit))
        #self.views.but_load.add_event(click_EventHandler(self.views.but_load, self.load))
        self.views.but_scanbarcode.add_event(click_EventHandler(self.views.but_scanbarcode, self.scanbarcode))
        self.views.but_copybarcode.add_event(click_EventHandler(self.views.but_copybarcode, self.copybarcode))
        self.views.data_list.add_event(itemclick_EventHandler(self.views.data_list, self.deletebarcode))

        pass

    def on_close(self):
        pass

    def load(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Load")

        saved_logo = qpy.tmp+"/qpy.logo"
        ur.urlretrieve("https://www.qpython.org/static/img_logo.png", saved_logo)
        self.views.logo.src = "file://"+saved_logo
        
    def scanbarcode(self,view,dummy):
        try:
            droid = FullScreenWrapper2App.get_android_instance()
            droid.makeToast("扫码")
            barcode = droid.scanBarcode()
            #print(barcode.result)
            self.scanbarcode_result_list.append(barcode.result)
            #self.views.scanbarcode_results.text="\n".join(self.scanbarcode_result_list)
            #print(dir(self.views.data_list))
            self.views.data_list.set_listitems(self.scanbarcode_result_list)
        except Exception as e:
            print("扫码错误：",str(e))
            droid.makeToast("扫码错误：",str(e))
            
    def copybarcode(self,view,dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.setClipboard("\n".join(self.scanbarcode_result_list))
        droid.makeToast("已复制到粘贴板")
        
    def deletebarcode(self,view,dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        #print(dummy.values())
        #print(list(dummy.values())[1]['position'])
        #droid.makeToast('delete'+str(list(dummy.values())[1]['position']))
        #print(type(list(dummy.values())[1]['position']))
        item=self.scanbarcode_result_list[int(list(dummy.values())[1]['position'])]
        a=self.Button('确认删除','从列表中删除{}'.format(item),('确定',))
        if not a.get('canceled'):
            a=a['which']
            if a=='positive':
                self.scanbarcode_result_list.pop(int(list(dummy.values())[1]['position']))
                self.views.data_list.set_listitems(self.scanbarcode_result_list)

    def exit(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("退出")
        FullScreenWrapper2App.close_layout()

if __name__ == '__main__':
    FullScreenWrapper2App.initialize(droid)
    FullScreenWrapper2App.show_layout(MainScreen())
    FullScreenWrapper2App.eventloop()
