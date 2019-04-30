#!/bin/bash -e

GEM_NAME=$1
PACKAGE_NAME=rubygem-$GEM_NAME
TEMPLATE_NAME=$2
TEMPLATE=$(pwd)/gem2rpm/$TEMPLATE_NAME.spec.erb
TITO_TAG=$3
DISTRO=${TITO_TAG##*-}
PACKAGE_SUBDIR=$4
ROOT=$(git rev-parse --show-toplevel)

if [[ -z $PACKAGE_DIR ]] ; then
	if [[ $TITO_TAG == foreman-plugins-* ]] ; then
		PACKAGE_SUBDIR="plugins"
	elif [[ $TITO_TAG == katello-* ]] ; then
		PACKAGE_SUBDIR="katello"
	else
		PACKAGE_SUBDIR="foreman"
	fi
fi

PACKAGE_DIR=packages/$PACKAGE_SUBDIR/$PACKAGE_NAME
SPEC_FILE="${PACKAGE_NAME}.spec"

if [[ -f "${PACKAGE_DIR}/${SPEC_FILE}" ]]; then
	echo "Detected update..."
	UPDATE=true
else
	UPDATE=false
fi

usage() {
	echo "Usage: $0 GEM_NAME TEMPLATE TITO_TAG [PACKAGE_SUBDIR]"
	echo "Valid templates: $(ls gem2rpm | sed 's/.spec.erb//' | tr '\n' ' ')"
	python -c "import ConfigParser ; c = ConfigParser.ConfigParser() ; c.read('rel-eng/tito.props') ; print 'Tito tags: ' + ' '.join(s for s in c.sections() if s not in ('requirements', 'buildconfig', 'builder'))"
	exit 1
}

generate_gem_package() {
	if [[ $UPDATE == true ]] ; then
		CHANGELOG=$(mktemp)
		sed -n '/%changelog/,$p' $PACKAGE_DIR/$SPEC_FILE > $CHANGELOG
		git rm -r $PACKAGE_DIR
	fi
	mkdir $PACKAGE_DIR
	pushd $PACKAGE_DIR
	gem2rpm -o $SPEC_FILE --fetch $GEM_NAME -t $TEMPLATE
	sed -i 's/\s\+$//' $SPEC_FILE
	git annex add *.gem

	VERSION=$(rpmspec --srpm -q --queryformat="%{version}-%{release}" --undefine=dist $SPEC_FILE)

	if [[ $UPDATE == true ]]; then
		cat $CHANGELOG >> $SPEC_FILE
		sed -i '/^%changelog/,/^%changelog/{0,//!d}' $SPEC_FILE
		rm $CHANGELOG
		CHANGELOG="- Update to $VERSION"
	else
		CHANGELOG="- Add $PACKAGE_NAME generated by gem2rpm using the $TEMPLATE_NAME template"
	fi
	echo "$CHANGELOG" | $ROOT/add_changelog.sh $SPEC_FILE

	git add $SPEC_FILE
	popd
}

add_to_tito_props() {
	# Get tito.props whitelists and add node package
	original_locale=$LC_COLLATE
	export LC_COLLATE=en_GB
	local current_whitelist=$(crudini --get rel-eng/tito.props $TITO_TAG whitelist)
	local whitelist=$(echo "$current_whitelist $PACKAGE_NAME" | tr " " "\n" | sort -u)
	crudini --set rel-eng/tito.props $TITO_TAG whitelist "$whitelist"
	export LC_COLLATE=$original_locale
	git add rel-eng/tito.props
}

add_gem_to_comps() {
	if [[ $TEMPLATE_NAME == "nonscl" ]] || [[ $TEMPLATE_NAME == "smart_proxy_plugin" ]] ; then
		local comps_scl="nonscl"
		local comps_package="${PACKAGE_NAME}"
	else
		local comps_scl=""
		local comps_package="tfm-${PACKAGE_NAME}"
	fi

	# TODO: figure this out for katello
	if [[ $TITO_TAG == foreman-plugins-* ]]; then
		local comps_file="foreman-plugins"
	else
		local comps_file="foreman"
	fi

	./add_to_comps.rb comps/comps-${comps_file}-${DISTRO}.xml $comps_package $comps_scl
	./comps_doc.sh
	git add comps/
}

add_to_manifest() {
	if [[ $TITO_TAG == "foreman-nightly-rhel7" ]] ; then
		local section="foreman_scl_packages"
	elif [[ $TITO_TAG == "foreman-nightly-nonscl-rhel7" ]] ; then
		local section="foreman_nonscl_packages"
	elif [[ $TITO_TAG == "foreman-plugins-nightly-rhel7" ]] ; then
		local section="plugin_scl_packages"
	elif [[ $TITO_TAG == "foreman-plugins-nightly-nonscl-rhel7" ]] ; then
		local section="plugin_nonscl_packages"
	elif [[ $TITO_TAG == "katello-nightly-rhel7" ]] ; then
		local section="katello_packages"
	else
		# TODO: client packages
		local section=""
	fi

	if [[ -n $section ]] ; then
		./add_host.py "$section" "$PACKAGE_NAME"
		git add package_manifest.yaml
	else
		echo "TODO: Add the package into the right section"
		echo "./add_host.py SECTION '$PACKAGE_NAME'"
		echo "git add package_manifest.yaml"
		echo "git commit --amend --no-edit"
	fi
}

# Main script

if [[ -z $GEM_NAME ]] || [[ -z $TEMPLATE_NAME ]] || [[ $UPDATE != true ]] && [[ -z $TITO_TAG ]]; then
	usage
fi

if [[ ! -e $TEMPLATE ]] ; then
	echo "Template $TEMPLATE does not exist."
	usage
	exit 1
fi

generate_gem_package
if [[ $UPDATE == true ]] ; then
	VERSION=$(rpmspec --srpm -q --queryformat="%{version}-%{release}" --undefine=dist $PACKAGE_DIR/$SPEC_FILE)
	git commit -m "Bump $PACKAGE_NAME to $VERSION"
else
	add_to_manifest
	add_to_tito_props
	add_gem_to_comps
	git commit -m "Add $PACKAGE_NAME package"
fi
