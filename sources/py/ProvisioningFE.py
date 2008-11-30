#!/bin/env python
from ProvCon.dbui.database import CFG
from ProvCon.dbui import meta, orm
from ProvCon.dbui import wxwin as guitk

import wx
from wx.lib import scrolledpanel as scrolled

class topwindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="ProvisioningFE", size=(600,400))
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer (wx.HORIZONTAL)
        lsizer = wx.BoxSizer ( wx.VERTICAL )
        self.tableeditor = guitk.complete.CompleteGenericForm ( self, tablename="table_info",
                                                                navigator = False)
        lsizer.Add (self.tableeditor, 4, flag=wx.EXPAND)
        
        self.fieldlist = guitk.recordlists.RecordList ([], self)        
        self.fieldlist.register_event_hook ( "current_record_changed", self.current_field_changed )
        lsizer.Add (self.fieldlist, 2, flag=wx.EXPAND)
        
        fieldinfotable = meta.Table.Get ( "field_info" )

        self.fieldrecords = orm.RecordList ( fieldinfotable, select=['name'], order="lp" )
        self.fieldrecords.filterfunc = lambda r: r.name not in meta.Table.__special_columns__
        
        self.tableeditor.form.register_event_hook ( "current_record_changed", self.current_table_changed )
        
        rsizer = wx.BoxSizer (wx.VERTICAL)
        self.fieldeditor = guitk.complete.CompleteGenericForm ( self, table = fieldinfotable,
                                                                navigator = False)
        rsizer.Add ( self.fieldeditor, 1, flag=wx.EXPAND )
        
        hsizer.Add(lsizer, 1, flag=wx.EXPAND)
        hsizer.Add(rsizer, 1, flag=wx.EXPAND)
        sizer.Add ( hsizer, 1, flag=wx.EXPAND)

        tablenav = guitk.navigators.Navigator (self)
        tablenav.set_records ( orm.RecordList ( self.tableeditor.table ).reload() )
        tablenav.navigate (1)
        sizer.Add (tablenav, 0, flag=wx.EXPAND)
        tablenav.Show()
        self.tableeditor.set_navigator ( tablenav )
        
        self.SetSizer (sizer)

    def current_table_changed(self, tablerecord):
        self.fieldrecords.filter = '"classid" = %d' % tablerecord.objectid
        self.fieldrecords.reload()
        self.fieldlist.set_records ( self.fieldrecords )
    
    def current_field_changed(self, field):
        if field:
            self.fieldeditor.navigate ( field.objectid )
        else:
            self.fieldeditor.navigate ( None )
        
        
app = wx.App()
top = topwindow()
top.Show()
app.MainLoop()






