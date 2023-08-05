# coding=utf8
## Copyright (c) 2020 Arseniy Kuznetsov
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.


from tabulate import tabulate   
from mktxp.cli.output.base_out import BaseOutputProcessor
from mktxp.datasource.dhcp_ds import DHCPMetricsDataSource
from mktxp.datasource.wireless_ds import WirelessMetricsDataSource


class WirelessOutput:
    ''' Wireless Clients CLI Output
    '''    
    @staticmethod
    def clients_summary(router_entry):
        registration_labels = ['interface', 'mac_address', 'signal_strength', 'uptime', 'tx_rate', 'rx_rate', 'signal_to_noise']
        registration_records = WirelessMetricsDataSource.metric_records(router_entry, metric_labels = registration_labels, add_router_id = False)
        if not registration_records:
            print('No wireless registration records')
            return 

        # translate / trim / augment registration records
        dhcp_lease_labels = ['host_name', 'comment', 'address', 'mac_address']
        dhcp_lease_records = DHCPMetricsDataSource.metric_records(router_entry, metric_labels = dhcp_lease_labels, add_router_id = False)   

        dhcp_rt_by_interface = {}
        for registration_record in sorted(registration_records, key = lambda rt_record: rt_record['signal_strength'], reverse=True):
            BaseOutputProcessor.augment_record(router_entry, registration_record, dhcp_lease_records)

            interface = registration_record['interface']
            if interface in dhcp_rt_by_interface.keys():
                dhcp_rt_by_interface[interface].append(registration_record)
            else:
                dhcp_rt_by_interface[interface] = [registration_record]         

        num_records = 0
        output_table = []
        for key in dhcp_rt_by_interface.keys():
            for record in dhcp_rt_by_interface[key]:
                output_table.append(BaseOutputProcessor.OutputWiFiEntry(**record))
                num_records += 1
            output_table.append({})
        print()
        print(tabulate(output_table, headers = "keys",  tablefmt="github"))
        print(tabulate([{0:'Connected Wifi Devices:', 1:num_records}], tablefmt="text"))
