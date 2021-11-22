#!/bin/bash
set -e

declare -A settings
name="leds"
configFile="$(pwd)/.install.cfg"
configurationString=""

requireRoot()
{
    if [ "$(id -u)" -ne "0" ] ; then
        echo "This script must be executed with root privileges."
        exit 1
    fi
}

installDocker()
{
    if [ ! -x "$(command -v docker)" ]
    then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        rm get-docker.sh
    fi
}

helpPrint()
{
    echo ""
    echo "Usage: $0 [-i][-r][-u][-h]"
    echo -e "\t-i pid=18,port=9000,ledCount=100:pid=21,port=9001,ledCount=30"
    echo -e "\t   Installs service with the provided configuration or reinstalls if .install.cfg already exists"
    echo -e "\t-r \n\t   Reinstalls current installation."
    echo -e "\t-u \n\t   Uninstall current installation."
    echo -e "\t-h \n\t   Display this help message"
    exit 1 # Exit script after printing help
}

parseCommands()
{
    instances=0
    configurations=$1
    readarray -d ":" -t configArray <<<"$configurations"
    for instanceCfgs in "${configArray[@]}"
    do
        instances=$((instances+1))
        readarray -d "," -t instanceArgs <<<"$instanceCfgs"

        for configs in "${instanceArgs[@]}"
        do
            readarray -d "=" -t configPair <<<"$configs"

            if [ ${#configPair[@]} != 2 ]; 
            then
                echo "Invalid key value pair, should be: key=value"
                exit 1
            fi
            
            key=${configPair[0]//$'\n'/}
            value=${configPair[1]//$'\n'/}

            if [ $key == "pid" ] || [ $key == "port" ] || [ $key == "ledCount" ]; 
            then
                if ! [[ $value =~ ^[0-9]+([.][0-9]+)?$ ]];
                then
                    echo "Invalid value provided, shoud be number!"
                    exit 1
                else
                    settings["${instances}-${key}"]+=$value
                fi
            else
                echo "Only \"pid\", \"port\" and \"ledCount\" keys are supported"
                exit 1
            fi
        done
    done
}

getInstallConfig()
{
    configString=""
    if test -f "$configFile"
    then
        configString="$(cat ${configFile})"
    fi

    if [ "$1" == "reinstall" ] && [ -z "$configString" ]
    then
        echo "Error: .install.cfg does not exist - nothing to reinstall"
        exit 1
    elif [ -n "$configString" ] && [ -n "$configurationString" ]
    then
        echo "Error: .install.cfg exists. Uninstall with: \"$0 -u\" or delete the file manually."
        exit 1
    elif [ -n "$configString" ]
    then
        echo ".install.cfg exists -> reinstalling existing installation with ${configString}."
        configurationString=$configString
    fi
}

createDockerNetwork()
{
    if [[ "$(docker network ls | grep ${name}-network)" == "" ]]
    then
        docker network create --driver bridge ${name}-network
    fi
}

installDockerContainers()
{
    for (( instance=1; instance <= $instances; ++instance ))
    do
        containerName="${name}-${instance}"
        pid=${settings["${instance}-pid"]}
        port=${settings["${instance}-port"]}
        ledCount=${settings["${instance}-ledCount"]}

        if systemctl --all --type service | grep -q "${name}-${instance}.service"
        then
            echo "Stopping & disabling service: ${name}-${instance}.service..."
            sudo systemctl stop ${name}-${instance}.service
            sudo systemctl disable ${name}-${instance}.service
        fi
        
        if [ "$(docker ps -a | grep ${name}-${instance})" ]
        then
            echo "Deleting container: ${name}-${instance}..."
            docker rm ${name}-${instance}
        fi

        echo "Building image: gradrix/${name}-${instance}..."
        docker build -t gradrix/${name}-${instance} --build-arg pid=${pid} --build-arg port=${port} --build-arg ledCount=${ledCount} .

        echo "Creating and running cointainer once..."
        docker run --name ${name}-${instance} -it --device /dev/gpiomem -p ${port}:${port} --privileged -d --restart unless-stopped --network ${name}-network gradrix/${name}-${instance}
    
        echo "Stopping container..."
        docker stop ${name}-${instance}

        installService ${name}-${instance}
    done
}

installService()
{
    service=$1

    echo "Adding ${service}.service file to systemd..."
    cat << EOF | sudo tee /lib/systemd/system/${service}.service
[Unit]
Description=${service} service
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=docker start -a ${service}
ExecStop=docker stop -t 2 ${service}

[Install]
WantedBy=default.target
EOF

    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload

    echo "Enabling ${service}.service"
    sudo systemctl enable ${service}.service

    echo "Starting ${service}.service"
    sudo systemctl start ${service}.service

    sleep 1

    if systemctl --state=failed --type service | grep -q "${service}.service"
    then
        echo "Service ${service}.service failed to start.."
        sudo systemctl status ${service}.service
        exit 1
    fi
}

install()
{
    getInstallConfig $1
    parseCommands $configurationString

    requireRoot
    installDocker
    
    createDockerNetwork
    installDockerContainers

    saveConfig
}

saveConfig()
{
    echo "Saving install config..."
    echo "$configurationString" | tee ${configFile}
}

handleCliCommands()
{
    while getopts "i:ruh" opt
    do
        case "$opt" in
            i ) 
                configurationString="$OPTARG" 
                install ;;
            r )
                install "reinstall" ;;
            h ) helpPrint ;; # Print helpFunction in case parameter is non-existent
        esac
    done

    # Print helpFunction in case parameters are empty
    if [ -z "$configurationString" ]
    then
        echo "Configurations were not provided!";
        helpPrint
    fi
}

handleCliCommands "$@"
