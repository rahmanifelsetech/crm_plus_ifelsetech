frappe.ui.form.on('CRM Deal', {
    refresh: function(frm) {
        // Add Create Event button
        frm.add_custom_button(__('Create Event'), function() {
            frappe.new_doc('Event', {
                crm_deal: frm.doc.name
            });
        }, __('Create'));

        // Add Create Project button
        frm.add_custom_button(__('Create Project'), function() {
            frappe.new_doc('CRM Project', {
                crm_deal: frm.doc.name
            });
        }, __('Create'));

        // Add View Events button
        frm.add_custom_button(__('View Events'), function() {
            frappe.route_options = {
                'crm_deal': frm.doc.name
            };
            frappe.set_route('List', 'Event');
        }, __('View'));

        // Add View Projects button
        frm.add_custom_button(__('View Projects'), function() {
            frappe.route_options = {
                'crm_deal': frm.doc.name
            };
            frappe.set_route('List', 'CRM Project');
        }, __('View'));
    }
});
